import os
from pathlib import Path

import evaluate
import kaggle
import numpy as np
from datasets import load_dataset
from transformers import (
    TrainingArguments,
    IntervalStrategy,
    Trainer,
    AutoImageProcessor,
    AutoModelForImageClassification,
)


DATASET_PATH = Path(__file__).resolve().parent / "dataset"

if not DATASET_PATH.exists():
    kaggle.api.authenticate()

    kaggle.api.dataset_download_files(
        "farzadnekouei/trash-type-image-dataset",
        path=str(DATASET_PATH),
        unzip=True,
    )

    kaggle.api.dataset_metadata(
        "farzadnekouei/trash-type-image-dataset", path=str(DATASET_PATH)
    )

dataset_folder = os.listdir(DATASET_PATH)[0]
image_dataset = DATASET_PATH / dataset_folder


dataset = load_dataset(
    "imagefolder",
    data_dir=str(DATASET_PATH),
)

processor = AutoImageProcessor.from_pretrained("yangy50/garbage-classification")

model = AutoModelForImageClassification.from_pretrained(
    "yangy50/garbage-classification",
    num_labels=len(dataset["train"].features["label"].names),
    ignore_mismatched_sizes=True,
)


def transform_images(pic: bytes):
    """ "Transforms raw image bytes to model inputs."""
    images = [img.convert("RGB") for img in pic["image"]]
    inputs = processor(images=images, return_tensors="pt")
    pic["pixel_values"] = inputs["pixel_values"]
    return pic


dataset = dataset.with_transform(transform_images)

accuracy = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=preds, references=labels)


training_args = TrainingArguments(
    output_dir="./app/AI/results",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    evaluation_strategy=IntervalStrategy.EPOCH,
    save_strategy=IntervalStrategy.EPOCH,
    logging_dir="./app/AI/logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=processor,
    compute_metrics=compute_metrics,
)


trainer.train()

model.save_pretrained("./app/AI/model")
processor.save_pretrained("./app/AI/model")
