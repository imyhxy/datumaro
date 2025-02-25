# Copyright (C) 2023 Intel Corporation
#
# SPDX-License-Identifier: MIT
import os.path as osp
from typing import Any, Dict

import numpy as np
import pytest

from datumaro.components.annotation import Bbox, Label, Polygon
from datumaro.components.dataset import Dataset
from datumaro.components.dataset_base import DatasetItem
from datumaro.components.importer import Importer
from datumaro.components.media import Image
from datumaro.plugins.data_formats.kaggle.base import *

from .base import TestDataFormatBase

from tests.utils.assets import get_test_asset_path
from tests.utils.test_utils import compare_datasets

DUMMY_DATASET_IMAGE_CSV_DIR = get_test_asset_path("kaggle_dataset", "image_csv")
DUMMY_DATASET_IMAGE_TXT_DIR = get_test_asset_path("kaggle_dataset", "image_txt")
DUMMY_DATASET_IMAGE_MASK = get_test_asset_path("kaggle_dataset", "image_mask")
DUMMY_DATASET_IMAGE_MASK_LABELMAP = get_test_asset_path(
    "kaggle_dataset", "image_mask_with_labelmap"
)
DUMMY_DATASET_VOC1_DIR = get_test_asset_path("kaggle_dataset", "relaxed_voc1")
DUMMY_DATASET_VOC2_DIR = get_test_asset_path("kaggle_dataset", "relaxed_voc2")
DUMMY_DATASET_YOLO_DIR = get_test_asset_path("kaggle_dataset", "relaxed_yolo")

IMAGE_DIR = "images"


@pytest.fixture
def fxt_img_dataset():
    return Dataset.from_iterable(
        [
            DatasetItem(
                id="1",
                subset="default",
                media=Image.from_numpy(data=np.ones((5, 10, 3))),
                annotations=[Label(label=0)],
            ),
            DatasetItem(
                id="2",
                subset="default",
                media=Image.from_numpy(data=np.ones((5, 10, 3))),
                annotations=[Label(label=1)],
            ),
            DatasetItem(
                id="3",
                subset="default",
                media=Image.from_numpy(data=np.ones((5, 10, 3))),
                annotations=[Label(label=0)],
            ),
            DatasetItem(
                id="4",
                subset="default",
                media=Image.from_numpy(data=np.ones((5, 10, 3))),
                annotations=[Label(label=1)],
            ),
            DatasetItem(
                id="5",
                subset="default",
                media=Image.from_numpy(data=np.ones((5, 10, 3))),
                annotations=[Label(label=1)],
            ),
        ],
        categories=["dog", "cat"],
    )


@pytest.fixture
def fxt_img_mask_dataset():
    colormap = {
        0: (0, 0, 0),  # background
        1: (255, 255, 255),  # cat
    }

    return Dataset.from_iterable(
        [
            DatasetItem(
                id="001",
                subset="default",
                media=Image.from_numpy(data=np.ones((1, 5, 3))),
                annotations=[
                    Mask(np.array([[0, 0, 1, 1, 0]]), label=0),
                    Mask(np.array([[1, 1, 0, 0, 1]]), label=1),
                ],
            ),
            DatasetItem(
                id="002",
                subset="default",
                media=Image.from_numpy(data=np.ones((1, 5, 3))),
                annotations=[
                    Mask(np.array([[1, 1, 0, 1, 0]]), label=0),
                    Mask(np.array([[0, 0, 1, 0, 1]]), label=1),
                ],
            ),
        ],
        categories={
            AnnotationType.label: LabelCategories.from_iterable(["background", "object"]),
            AnnotationType.mask: MaskCategories(colormap),
        },
    )


@pytest.fixture
def fxt_img_mask_labelmap_dataset():
    colormap = {
        0: (0, 0, 0),  # background
        1: (255, 0, 0),  # cat
        2: (0, 255, 0),  # dog
    }

    return Dataset.from_iterable(
        [
            DatasetItem(
                id="001",
                subset="default",
                media=Image.from_numpy(data=np.ones((1, 5, 3))),
                annotations=[
                    Mask(np.array([[0, 0, 1, 0, 0]]), label=0),
                    Mask(np.array([[1, 0, 0, 0, 1]]), label=1),
                    Mask(np.array([[0, 1, 0, 1, 0]]), label=2),
                ],
            ),
            DatasetItem(
                id="002",
                subset="default",
                media=Image.from_numpy(data=np.ones((1, 5, 3))),
                annotations=[
                    Mask(np.array([[1, 1, 0, 1, 0]]), label=0),
                    Mask(np.array([[0, 0, 0, 0, 1]]), label=1),
                    Mask(np.array([[0, 0, 1, 0, 0]]), label=2),
                ],
            ),
            DatasetItem(
                id="003",
                subset="default",
                media=Image.from_numpy(data=np.ones((1, 5, 3))),
                annotations=[
                    Mask(np.array([[0, 0, 1, 1, 1]]), label=0),
                    Mask(np.array([[0, 1, 0, 0, 0]]), label=1),
                    Mask(np.array([[1, 0, 0, 0, 0]]), label=2),
                ],
            ),
        ],
        categories={
            AnnotationType.label: LabelCategories.from_iterable(["background", "cat", "dog"]),
            AnnotationType.mask: MaskCategories(colormap),
        },
    )


@pytest.fixture
def fxt_voc_dataset():
    return Dataset.from_iterable(
        [
            DatasetItem(
                id="2007_000001",
                subset="default",
                media=Image.from_numpy(data=np.ones((10, 20, 3))),
                annotations=[
                    Bbox(
                        1.0,
                        2.0,
                        2.0,
                        2.0,
                        label=0,
                        id=0,
                    ),
                    Bbox(
                        4.0,
                        5.0,
                        2.0,
                        2.0,
                        label=1,
                        id=1,
                    ),
                ],
            ),
            DatasetItem(
                id="2007_000002",
                subset="default",
                media=Image.from_numpy(data=np.ones((10, 20, 3))),
            ),
        ],
        categories=["cat", "person"],
    )


@pytest.fixture
def fxt_yolo_dataset():
    return Dataset.from_iterable(
        [
            DatasetItem(
                id=1,
                subset="default",
                media=Image.from_numpy(data=np.ones((10, 15, 3))),
                annotations=[
                    Bbox(0, 2, 4, 2, label=0, id=0),
                    Bbox(3, 3, 2, 3, label=1, id=1),
                ],
            ),
            DatasetItem(
                id=2,
                subset="default",
                media=Image.from_numpy(data=np.ones((10, 15, 3))),
                annotations=[
                    Bbox(0, 2, 4, 2, label=2, id=0),
                    Bbox(3, 3, 2, 3, label=3, id=1),
                ],
            ),
        ],
        categories=["2", "4", "1", "3"],
    )


IDS = [
    "IMAGE_CSV",
    "IMAGE_CSV_WO_EXT",
    "IMAGE_TXT",
    "IMAGE_TXT_WO_EXT",
    "IMAGE_MASK",
    "IMAGE_MASK_LABELMAP",
    "VOC1",
    "VOC2",
    "YOLO",
]


@pytest.mark.new
class KaggleImporterTest(TestDataFormatBase):
    @pytest.mark.parametrize("fxt_dataset_dir", [DUMMY_DATASET_IMAGE_CSV_DIR])
    def test_can_detect(self, fxt_dataset_dir: str):
        return super().test_can_detect(fxt_dataset_dir, None)

    @pytest.mark.parametrize(
        [
            "fxt_dataset_dir",
            "fxt_img_path",
            "fxt_expected_dataset",
            "importer",
            "fxt_import_kwargs",
        ],
        [
            (
                DUMMY_DATASET_IMAGE_CSV_DIR,
                "images",
                "fxt_img_dataset",
                KaggleImageCsvBase,
                {
                    "ann_file": osp.join(DUMMY_DATASET_IMAGE_CSV_DIR, "ann.csv"),
                    "columns": {"media": "image_name", "label": "label_name"},
                },
            ),
            (
                DUMMY_DATASET_IMAGE_CSV_DIR,
                "images",
                "fxt_img_dataset",
                KaggleImageCsvBase,
                {
                    "ann_file": osp.join(DUMMY_DATASET_IMAGE_CSV_DIR, "ann_wo_ext.csv"),
                    "columns": {"media": "image_name", "label": "label_name"},
                },
            ),
            (
                DUMMY_DATASET_IMAGE_TXT_DIR,
                "images",
                "fxt_img_dataset",
                KaggleImageTxtBase,
                {
                    "ann_file": osp.join(DUMMY_DATASET_IMAGE_TXT_DIR, "ann.txt"),
                    "columns": {"media": 0, "label": 1},
                },
            ),
            (
                DUMMY_DATASET_IMAGE_TXT_DIR,
                "images",
                "fxt_img_dataset",
                KaggleImageTxtBase,
                {
                    "ann_file": osp.join(DUMMY_DATASET_IMAGE_TXT_DIR, "ann_wo_ext.txt"),
                    "columns": {"media": 0, "label": 1},
                },
            ),
            (
                DUMMY_DATASET_IMAGE_MASK,
                "images",
                "fxt_img_mask_dataset",
                KaggleImageMaskBase,
                {"mask_path": osp.join(DUMMY_DATASET_IMAGE_MASK, "masks")},
            ),
            (
                DUMMY_DATASET_IMAGE_MASK_LABELMAP,
                "images",
                "fxt_img_mask_labelmap_dataset",
                KaggleImageMaskBase,
                {
                    "mask_path": osp.join(DUMMY_DATASET_IMAGE_MASK_LABELMAP, "masks"),
                    "labelmap_file": osp.join(DUMMY_DATASET_IMAGE_MASK_LABELMAP, "labelmap.csv"),
                },
            ),
            (
                DUMMY_DATASET_VOC1_DIR,
                "images",
                "fxt_voc_dataset",
                KaggleVocBase,
                {"ann_path": osp.join(DUMMY_DATASET_VOC1_DIR, "annotations")},
            ),
            (
                DUMMY_DATASET_VOC2_DIR,
                "",
                "fxt_voc_dataset",
                KaggleVocBase,
                {"ann_path": DUMMY_DATASET_VOC2_DIR},
            ),
            (
                DUMMY_DATASET_YOLO_DIR,
                "",
                "fxt_yolo_dataset",
                KaggleYoloBase,
                {"ann_path": DUMMY_DATASET_YOLO_DIR},
            ),
        ],
        indirect=["fxt_expected_dataset"],
        ids=IDS,
    )
    def test_can_import(
        self,
        fxt_dataset_dir: str,
        fxt_img_path: str,
        fxt_expected_dataset: Dataset,
        fxt_import_kwargs: Dict[str, Any],
        request: pytest.FixtureRequest,
        importer: Importer,
    ):
        helper_tc = request.getfixturevalue("helper_tc")
        dataset = Dataset.import_from(
            path=osp.join(fxt_dataset_dir, fxt_img_path), format=importer.NAME, **fxt_import_kwargs
        )

        compare_datasets(helper_tc, fxt_expected_dataset, dataset, require_media=False)
