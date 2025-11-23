import os
from pathlib import Path
from typing import List

import evaluate
import kaggle
import numpy as np
import torch
from datasets import load_dataset, ClassLabel, DatasetDict
from transformers import (
    TrainingArguments,
    Trainer,
    AutoImageProcessor,
    IntervalStrategy,
    AutoModelForImageClassification,
)


KNOWN_CLASS_NAMES = {"cardboard", "glass", "metal", "paper", "plastic", "trash"}
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def ensure_dataset(base_dir: Path) -> None:
    """Download and unzip the Kaggle dataset if base_dir doesn't exist."""
    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "farzadnekouei/trash-type-image-dataset",
            path=str(base_dir),
            unzip=True,
        )
        kaggle.api.dataset_metadata(
            "farzadnekouei/trash-type-image-dataset", path=str(base_dir)
        )


def immediate_subdirs(p: Path) -> List[Path]:
    """Return immediate subdirectories of p."""
    try:
        return [d for d in p.iterdir() if d.is_dir()]
    except PermissionError:
        return []


def looks_like_class_root(p: Path) -> bool:
    """Heuristic to decide if p contains class folders."""
    subs = immediate_subdirs(p)
    if len(subs) < 2:
        return False
    names = {d.name.lower() for d in subs}
    if len(names & KNOWN_CLASS_NAMES) >= 2:
        return True
    hits = 0
    for d in subs:
        try:
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() in IMG_EXTS:
                    hits += 1
                    break
        except PermissionError:
            continue
    return hits >= 2


def find_class_root(base_dir: Path) -> Path:
    """Find the directory under base_dir that actually contains class folders."""
    if looks_like_class_root(base_dir):
        return base_dir
    for depth in range(1, 5):
        for p in base_dir.rglob("*"):
            if not p.is_dir():
                continue
            try:
                if len(p.relative_to(base_dir).parts) > depth:
                    continue
            except Exception:
                continue
            if looks_like_class_root(p):
                return p
    raise FileNotFoundError(f"Could not locate class root under {base_dir}")


def make_batched_transform(processor):
    """Return a transform that outputs per-example pixel_values and labels."""

    def _t(batch):
        imgs = batch["image"]
        if isinstance(imgs, list):
            imgs = [im.convert("RGB") for im in imgs]
            pv = processor(images=imgs, return_tensors="pt")["pixel_values"]
            batch["pixel_values"] = [pv[i] for i in range(pv.shape[0])]
            batch["labels"] = batch["label"]
            return batch
        pv = processor(images=imgs.convert("RGB"), return_tensors="pt")["pixel_values"][
            0
        ]
        batch["pixel_values"] = pv
        batch["labels"] = batch["label"]
        return batch

    return _t


def data_collator(examples):
    """Stack pixel_values and labels; ignore raw images."""
    pixel_values = torch.stack([e["pixel_values"] for e in examples])
    labels = torch.tensor(
        [e["labels"] if "labels" in e else e["label"] for e in examples]
    )
    return {"pixel_values": pixel_values, "labels": labels}


def build_splits(class_root: Path) -> DatasetDict:
    """Create train/test: train excludes 'trash'; test = class_root/trash if it has subfolders."""
    full = load_dataset("imagefolder", data_dir=str(class_root))["train"]

    orig_names = full.features["label"].names
    id2name = {i: n for i, n in enumerate(orig_names)}
    keep_names = [n for n in orig_names if n.lower() != "trash"]
    name_to_new = {name: i for i, name in enumerate(keep_names)}

    train_ds = full.filter(lambda x: id2name[x["label"]].lower() != "trash")
    train_ds = train_ds.map(lambda ex: {"label": name_to_new[id2name[ex["label"]]]})
    train_ds = train_ds.cast_column("label", ClassLabel(names=keep_names))

    trash_dir = class_root / "trash"
    test_ds = None
    if trash_dir.exists():
        subs = immediate_subdirs(trash_dir)
        if len(subs) >= 1:
            test_raw = load_dataset(
                "imagefolder", data_dir=str(trash_dir), split="train"
            )
            test_names = test_raw.features["label"].names
            test_ds = test_raw.map(
                lambda ex: {"label": name_to_new.get(test_names[ex["label"]], -1)}
            )
            test_ds = test_ds.filter(lambda x: x["label"] != -1)
            if len(test_ds) > 0:
                test_ds = test_ds.cast_column("label", ClassLabel(names=keep_names))
            else:
                test_ds = None

    return DatasetDict(
        {"train": train_ds, **({"test": test_ds} if test_ds is not None else {})}
    )


def main():
    DATASET_PATH = Path(__file__).resolve().parent / "dataset"
    ensure_dataset(DATASET_PATH)

    class_root = find_class_root(DATASET_PATH)
    print(f"[ROOT] {class_root}")

    dataset = build_splits(class_root)
    print(dataset)

    processor = AutoImageProcessor.from_pretrained("yangy50/garbage-classification")
    dataset = dataset.with_transform(make_batched_transform(processor))

    label_names = dataset["train"].features["label"].names
    id2label = {i: n for i, n in enumerate(label_names)}
    label2id = {n: i for i, n in id2label.items()}

    model = AutoModelForImageClassification.from_pretrained(
        "yangy50/garbage-classification",
        num_labels=len(label_names),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    accuracy = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        if isinstance(logits, tuple):
            logits = logits[0]
        preds = np.argmax(logits, axis=-1)
        return accuracy.compute(predictions=preds, references=labels)

    os.makedirs("./app/AI/results", exist_ok=True)
    os.makedirs("./app/AI/logs", exist_ok=True)
    os.makedirs("./app/AI/model", exist_ok=True)

    has_test = "test" in dataset

    training_args = TrainingArguments(
        output_dir="./app/AI/results",
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        eval_strategy=IntervalStrategy.EPOCH if has_test else IntervalStrategy.NO,
        save_strategy=IntervalStrategy.EPOCH,
        logging_dir="./app/AI/logs",
        logging_steps=10,
        load_best_model_at_end=has_test,
        metric_for_best_model="accuracy",
        remove_unused_columns=False,
        dataloader_pin_memory=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"] if has_test else None,
        tokenizer=processor,
        compute_metrics=compute_metrics if has_test else None,
        data_collator=data_collator,
    )
    model_path = Path(__file__).resolve().parent / "model"
    trainer.train()
    model.save_pretrained(model_path)
    processor.save_pretrained(model_path)
    print("Saved at file://{model_path}")


if __name__ == "__main__":
    main()
