import os
import random
import sys
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

import transformers
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EvalPrediction,
    HfArgumentParser,
    PretrainedConfig,
    Trainer,
    TrainingArguments,
    default_data_collator,
    set_seed,
)
from modeling_electra import ElectraForSequenceClassification
from transformers.trainer_utils import get_last_checkpoint
from transformers.utils import check_min_version, send_example_telemetry
from transformers.utils.versions import require_version

import torch
import torch.nn.functional as F
from lime.lime_text import LimeTextExplainer
from transformers import pipeline


if __name__ == "__main__":
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}
    cls_pipe = pipeline("text-classification",model="weights/v1_2000_epochs",**tokenizer_kwargs, return_all_scores=True)

    lable = ['10', '2', '3.1(Cuc CNTT 2023)', 'CCDS.I.1', 'CCDS.I.11', 'CCDS.I.12', 'CCDS.I.15', 'CCDS.I.6', 'CCDS.I.8', 'CCDS.II.5', 'CCDS.II.7', 'CCDS.III.1.2', 'CCDS.III.1.4', 'CCDS.III.1.6', 'CCDS.III.1.9', 'CCDS.IV.2', 'CCDS.IX.2.1', 'CCDS.V', 'CCDS.V.1', 'CCDS.V.3', 'CCDS.V.4', 'CCDS.V.5', 'CCDS.V.6', 'CCDS.V.8', 'CCDS.VI.1', 'CCDS.VI.2', 'CCDS.VI.3', 'CCDS.VI.4', 'CCDS.VI.5.2', 'CCDS.VI.6', 'CCDS.VII.2', 'CCDS.VII.2.1', 'CCDS.VII.2.3', 'CCDS.VII.3.3', 'CCDS.XI.1.1', 'CCDS.XII', 'CCDS.XII.12', 'CCDS.XII.13', 'CCDS.XII.14', 'CCDS.XII.15', 'CCDS.XII.16', 'CCDS.XII.18', 'CCDS.XII.19', 'CCDS.XII.20', 'CCDS.XII.21', 'CCDS.XII.23', 'CCDS.XII.24', 'CCDS.XII.4', 'CCDS.XII.7', 'CCNTT.KHCN-ATTT.2022.II.1.1', 'CCNTT.KHCN-ATTT.2022.II.1.7', 'CDS.A.I.1.2', 'CDS.A.I.1.3', 'CDS.A.I.1.4', 'CDS.A.I.1.6', 'CDS.A.I.3', 'CDS.A.II.1.1', 'CDS.A.II.1.1\n  CDS.A.II.1.2', 'CDS.A.II.1.2', 'CDS.A.II.1.3', 'CDS.A.II.1.4', 'CDS.A.II.1.5', 'CDS.A.II.2.3', 'CDS.A.II.3', 'CDS.A.II.4.1', 'CDS.A.II.4.3', 'CDS.A.II.4.4', 'CDS.A.II.4.7', 'CDS.A.II.5', 'CDS.A.II.6', 'CDS.A.II.7', 'CDS.C.1', 'CDS.C.3', 'CDS.C.4', 'CDS.D.1', 'CDS.D.2.1', 'CDS.D.2.2', 'CDS.D.2.4', 'CDS.D.2.6', 'CDS.D.2.7', 'CDS.D.2.7\n  CDS.D.2.3', 'CDS.I.5', 'CDS.TTDL-TNMT.I.1', 'CMPM.-NTS.XI.1.1', 'CMPM.-NTS.XI.3', 'CMPM.-NTS.XI.4', 'CNMP.A.II', 'CNMP.B.1.2', 'CNMP.B1.1', 'CNMP.B1.1\n  CNMP.B.1.2', 'CNMP.B1.1\n  CNMP.B.1.3', 'CNMP.C.a.1.1.2.2', 'CNMP.C.b.1', 'CNMP.C.b.1.1.2.2', 'CNMP.C.b.1.1.2.3', 'CNMP.E.3.3', 'CNMP.E.5', 'CNNV.TTKDSPCNTT.2.1', 'CNNV.TTKDSPCNTT.2.2', 'CNPM-NTS.II.1', 'CNPM-NTS.VI', 'CNPM-NTS.X.b.1', 'CNTT2023-TTDKPM.1.1', 'CSHT.A', 'CSHT.B..1', 'CSHT.B.1', 'CSHT.B.2', 'CSHT.B.III.4', 'CSHT.B.V.1', 'HTTT.CNNV.13', 'HTTT.I.1.4', 'HTTT.I.2', 'HTTT.I.3.', 'HTTT.I.3.2', 'HTTT.I.3.3', 'HTTT.I.3.4', 'HTTT.I.3.6', 'HTTT.I.3.7', 'HTTT.I.3.7..b', 'HTTT.I.3.7.a', 'HTTT.I.3.8', 'HTTT.I.3.8.a', 'HTTT.I.3.8.c', 'HTTT.I.3.8.d', 'HTTT.I.4.4.1', 'HTTT.I.4.4.2', 'HTTT.I.5.1', 'HTTT.I.5.2', 'HTTT.I.5.3\n  HTTT.I.3.7..b', 'HTTT.I.6', 'HTTT.II.1', 'HTTT.II.1.1', 'HTTT.II.2', 'HTTT2022.VI.1', 'II.2', 'IV', 'KDPM.1', 'KHCN-ATTT.C1', 'KHCN-ATTT.D.13', 'KHCN-ATTT.D.2', 'KHCN-ATTT.D.2.1', 'KHCN-ATTT.D.2.3', 'KHCN-ATTT.D.2.4', 'KHCN-ATTT.D.3', 'KHCN-ATTT.D.5', 'KHCN-ATTT.D.7', 'KHCN-ATTT.D.9', 'KHCN.ATTT.A.I.1.1', 'KHCN.ATTT.A.I2.1', 'KHCN.ATTT.A.II.1.8', 'KHCN.ATTT.A.II.1.9', 'KHCN.ATTT.A.II.2', 'KHCN.ATTT.A.II.3.2', 'KHCN.ATTT.A.II.3.3', 'KHCN.ATTT.A.II.4.1', 'KHCN.ATTT.A.II.4.3', 'KHCN.ATTT.A1.1', 'KHTC.1', 'KHTC.3.b', 'KHTC.3.c', 'KHTC.4.a', 'KHTC.4.c', 'KHTC.5.a', 'KHTC.5.b', 'KHTC.6', 'KHTC.7', 'LTTV.VIII.3', 'LTTV.XII', 'PPC.I.1.4', 'PPC.I.1.5', 'PPC.I.1.8', 'PPC.I.2', 'PPC.I.2.1', 'PPC.I.2.2', 'PPC.I.4', 'PPC.II.11', 'PPC.III', 'PPC.V', 'PPC.VI.1', 'PPC.VI.2', 'PPC.VI.3', 'PPC.VII', 'TTLT-TVTNMTQG.CNNV.1a', 'V', 'VI', 'VIII.3.1', 'VIII.3.1, VIII.3.2', 'VPC.CNNV.1d', 'VPC.I.', 'VPC.I.1', 'VPC.I.2', 'VPC.I.5', 'VPC.I.6', 'VPC.I.7', 'VPC.I.7 7', 'VPC.II', 'VPC.II.10', 'VPC.II.11', 'VPC.II.12', 'VPC.II.12\n VPC.II.14', 'VPC.II.13', 'VPC.II.14', 'VPC.II.15', 'VPC.II.16', 'VPC.II.17', 'VPC.II.18', 'VPC.II.9', 'VPC.III', 'VPC.III.19', 'VPC.III.20', 'VPC.III.21', 'VPC.III.22', 'VPC.IV.24', 'VPC.IV.25', 'VPC.V', 'VPC.V.26', 'VPC.V.28', 'VPC.VI', 'VPC.VI.29', 'VPC.VII.32', 'VPC.VII.33', 'VPC.VII.34', 'VPC.VII.35', 'VPC.VII.37', 'VPC.VII.39', 'unknow']

    explainer = LimeTextExplainer(class_names=lable)

    text_test = "BỘ  TÀI  NGUYÊN  VÀ  MỖI  TRƯỜNG. \nCỘNG  HÒA  XÃ  HỘI  CHỦ  NGHĨA  VIỆT  NAM \nVỤ  KẾ  HOẠCH  -  TÀI  CHÍNH \nĐộc  lập  -  Tự  do  -  Hạnh  phức \nSố:  15/KHTC-KHTH \nHà  Nội,  ngày  09  tháng  01  năm  2023 \nTHÔNG  BÁO \nVề  việc  phân  công  nhiệm  vụ \ncủa  Lãnh  đạo  Vụ  Kế  hoạch  -  Tài  chính \nCăn  cứ  Quyết  định  số  2899/QĐ-BTNMT  ngày  28  tháng  10  năm  2022  của \nBộ  trưởng  Bộ  Tài  nguyên  và  Môi  trường  quy  định  chức  năng,  nhiệm  vụ,  quyền \nhạn  và  cơ  cấu  tổ  chức  của  Vụ  Kế  hoạch -  Tài  chính,  Vụ  Kế  hoạch -  Tải  chính \nphân  công  nhiệm  vụ  đối  với  các  Lãnh  đạo  Vụ  như  sau: \n1,  Phân  công  nhiệm  vụ \n1.1.  Vụ  trướng  Đặng  Ngọc  Diệp \na)  Chỉ  đạo  điều  hành  toàn  diện  các  hoạt  động  của  Vụ  theo  chức  năng, \nnhiệm  vụ  của  Vụ  được  giao  và  thực  hiện  các  quy  định  thuộc  thâm  quyên  giải \nquyêt  của  Vụ  trưởng. \nb)  Trực  tiếp  chỉ  đạo: \n-  Xây  dựng,  theo  dõi  tình  hình  thực  hiện  chiến  lược,  quy  hoạch,  kế  hoạch \nphát  triển  ngành  tài  nguyên  và  môi  trường. \n-  Xây  dựng  hoặc  góp  ý  kiến,  hướng  dẫn  thực  hiện  cơ  chế  chính  sách \nchung  vê:  công  tác  kê  hoạch;  tài  chính;  đâu  tư;  quản  lý  tài  sản  nhà  nước  đôi  với \ncác  lĩnh  vực  thuộc  phạm  vi  quản  lý  nhà  nước  của  Bộ. \n-  Tổng  hợp:  xây  dựng,  phân  bồ,  giao,  điều  chỉnh  dự  toán  ngân  sách  nhà  nước. \n-  Các  dự  án  sử  dụng  nguồn  vốn  đầu  tư  phát  triển;  các  chương  trình,  dự  án \ncó  nhiêu  lĩnh  vực  thuộc  Bộ  cùng  thực  hiện. \n-  Công  tác  điều  phối  phát  triển  các  vùng  kinh  tế  -  xã  hội. \n-  Công  tác  tổ  chức  và  quản  lý  cán  bộ,  công  chức;  tiết  kiệm,  phòng  chống \ntham  nhũng.  tham  ô,  lãng  phí;  công  tác  cải  cách  hành  chính;  thi  đua  khen  thưởng: \nthanh  tra,  kiêm  tra;  ứng  dụng  công  nghệ  thông  tín  của  Vụ. \nc)  Quản  lý  công  tác  kế  hoạch,  tài  chính  đơn  vị:  Ban  Quản  lý  dự  án  đầu  tư \nxây  dựng  Bộ  Tải  nguyên  và  Môi  trường. \nd)  Thực  hiện  các  nhiệm  vụ  khác  theo  phân  công  của  Lãnh  đạo  Bộ. \ne)  Vụ  trưởng  ủy  nhiệm  các  Phó  Vụ  trưởng  giải  quyết  và  ký  một  số  văn \nbản  thuộc  trách  nhiệm  của  Vụ  trưởng  về  công  tác  kê  hoạch,  tài  chính,  đâu  tư, \nquản  lý  tài  sản  nhà  nước  và  các  công  tác  khác  đôi  với  các  lĩnh  vực  thuộc  phạm \nvĩ  quản  lý  nhà  nước  của  Bộ."

    #text_test = "Phê duyệt Đề án tổng kiểm kê tài nguyên nước quốc gia, giai đoạn \
    #đến năm 2025 (sau đây gọi tắt là Đề án) với những nội dung chính như sau:"

    #text_test = "BỘ TÀI NGUYÊN VÀ MỖI TRƯỜNG. \nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \nVỤ KẾ HOẠCH"

    text_test = "BỘ TÀI NGUYÊN VÀ MỖI TRƯỜNG. \nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \nVỤ KẾ HOẠCH"

    
    index_label = []
    def predictor(texts):
        print("len(texts):",len(texts))
        prediction = cls_pipe(texts)
        print("type(prediction):",type(prediction))
        print("max:",max(prediction[0], key=lambda k: k["score"]))
        label = max(prediction[0], key=lambda k: k["score"])["label"]
        index_label = lable.index(label)
        print("index_label:",index_label)
        print("len(prediction2.0):",len(prediction))
        probability = []
        for p in prediction:
            pro = []
            for i in p:
                pro.append(i["score"])
            probability.append(pro)
        print("len(probability):",len(probability))
        probability = np.array(probability)
        print("probability.shape:",probability.shape)
        return probability
    
    exp = explainer.explain_instance(text_test, predictor, num_features=20,num_samples=100, top_labels=2)
    print("index_label:",index_label)
    print("exp.as_list:",exp.as_list(225))
