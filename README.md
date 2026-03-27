[![DOI](https://zenodo.org/badge/1091649334.svg)](https://doi.org/10.5281/zenodo.19254583)

This `README` file is given in [English](#preamplifier-decouplinggain-and-impedance-matching-network-calculator-english) and [Classical Chinese](#前放大器釋耦暨阻抗匹配網絡計算器漢語). For the Classical Chinese version, scroll down. 

此`README`文件有[英語](#preamplifier-decouplinggain-and-impedance-matching-network-calculator-english)與[古典漢語](#前放大器釋耦暨阻抗匹配網絡計算器漢語)版本。漢語版本在下。


# Preamplifier Decoupling/Gain and Impedance Matching Network Calculator (English)
Author: WÁNG, Wénjùn (王文俊)

> I have heard that one brings harmony to the people through virtue, but never through disorder. Using disorder to quell disorder is like trying to untangle silk threads only to end up knotting them further. <br/>
> —Chūn Qiū Zuǒ Zhuàn, Duke Yǐn Year 4; 709 BCE (春秋左傳・隱公四年)

This repository serves two purposes: 
1. **Three- and four-element matching networks** that present high or low input impedance, which allows for suppressing coil loop current or designing low-impedance amplifiers;
2. **Preamplifier decoupling/gain vs noise figure trade-off**, which allows for picking the right operating point for the best balance between preamplifier decoupling/gain and noise figure.
They implement the algorithm and formulae in [reference \[1\]](#references). Although [reference \[1\]](#references) talks about the trade-off between preamplifier decoupling and noise figure, it may also be used for computing the trade-off between amplifier gain and noise figure (See [Theory](./docs/Theory.md)).

A web version of the three- and four-element network calculator is found on [DTU RF Toolbox](https://rftoolbox.dtu.dk/rfcalc/NoiseMatching.html).

## Installation
1. Install [Python](https://www.python.org/) (at least 3.11) and [Git](https://git-scm.com/). 
2. Run in command line the following, one command each time: <br/>
```powershell
git clone https://github.com/wenjunhj/impedance-matching-and-preamplifier-decoupling
# Alternatively, download the GitHub repository directly into any folder.
cd ./impedance-matching-and-preamplifier-decoupling
pip install -r requirements.txt
```

## Basic Use
There are three Jupyter notebooks under `.\examples`:
- `three_element_network.ipynb`: calculating three-element preamplifier-decoupling-matching networks;
- `four_element_network.ipynb`: calculating four-element preamplifier-decoupling-matching networks;
- `preamplifier_decoupling_and_gain_vs_noise_figure.ipynb`: computing the tradeoff between the preamplifier decoupling and noise figure, or the tradeoff between amplifier gain and noise figure. 

These notebooks call the functions in `amplifier.py`, `conversion.py`, `matching_decoupling_network.py`.

## Table of Contents
- [Acronyms](#acronyms-and-glossary)
- [Double-Loop H-Field Probe Calibration](#double-loop-h-field-probe-calibration)
- [Usage](./docs/Usage.md)
	- [Three- and Four-Element Matching Networks for High or Low Impedance](./docs/Usage.md#three--and-four-element-matching-networks-for-high-or-low-impedance)
	- [Preamplifier Decoupling/Gain vs Noise Figure Trade-Off](./docs/Usage.md#preamplifier-decouplinggain-vs-noise-figure-trade-off)
- [Special Notes on Camel-Hump Responses](./docs/Special_Notes_on_Camel-Hump_Responses.md)
- [Practicalities](./docs/Practicalities.md)
- [Theory](./docs/Theory.md)
- [Other Notes](#other-notes)
- [References](#references)

## Acronyms and Glossary

| Acronym | Meaning                      |
| ------- | ---------------------------- |
| DC      | direct current               |
| DF      | dissipation factor           |
| ESR     | equivalent series resistance |
| MR      | magnetic resonance           |
| MRI     | magnetic resonance imaging   |
| PCB     | printed circuit board        |
| Q       | quality factor               |
| SNR     | signal-to-noise ratio        |
| SWR     | standing wave ratio          |
| VNA     | vector network analyzer      |

Also in this GitHub repository: 
- "Matching", "impedance matching" and "impedance transform" are used interchangeably.
- "Preamplifier" and "amplifier" are used interchangeably.


## Double-Loop H-Field Probe Calibration
To experimentally observe preamplifier decoupling, a calibration method for double-loop H-field probes is recommended: 
- Connect a double loop probe to a VNA. Tighten all connections. Use a torque wrench whenever required. Secure the positions of the probe and the cable. Ensure that the double-loop probe and all the cables remain in the same place throughout all measurements.
- Remove the MR coil (loop antenna). Record the $S_{21}$ measurement results in the complex format as $S_{21,a}$.
- Put back the MR coil. Record the $S_{21}$ measurement results in the complex format  as $S_{21,b}$.
- Take the complex-number difference $S_{21,\mathrm{cal}}=S_{21,b}-S_{21,a}$.

When implementing this calibration method on a VNA, one can use the trace math function. For a better dynamic ranges, turn on averaging for the double-loop only, coil-free measurement. [Here is an example](docs/Double_Loop_Calibration__ZNL3__Rohde_Schwarz.md) on a Rohde-Schwarz ZNL3 vector network analyzer. 

This calibration corrects for residual probe coupling and improves the dynamic range of detection. There is 
```math
S_{21,\mathrm{cal}} \approx \mathrm{j} \omega \kappa \mathrm{e}^{\mathrm{j} \omega \tau} \cdot I_\mathrm{loop} ,
```
where $\kappa<0$, $\tau<0$ are some setup-specific constants that generally need not be known, $I_\mathrm{loop}$ is the loop coil current. For more information, refer to [reference \[2\]](#references).

## Usage
Read [here](./docs/Usage.md).

## Special Notes on Camel-Hump Responses
Read [here](./docs/Special_Notes_on_Camel-Hump_Responses.md).

## Practicalities
Read [here](./docs/Practicalities.md).

## Theory
Read [here](./docs/Theory.md).

## Other Notes
Related funding:
- Danmarks Grundforskningsfond (Danish National Research Foundation), DNRF-124
- European Research Council (ERC) Synergy grant 856432—HyperQ
- Innovation Fund Denmark grant E2409

## References
For all the references, go to the [master reference list](./docs/References.md).

1. W. Wang, V. Zhurbenko, J. D. Sánchez-Heredia, and J. H. Ardenkjær-Larsen. “Trade-off between preamplifier noise figure and decoupling in MRI detectors”. In: Magnetic Resonance in Medicine 89 (2 Feb. 2023), pp. 859–871. ISSN: 15222594. DOI: 10.1002/mrm.29489. 
   - [Open Access](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.29489). 
2. W. Wang, J. D. Sánchez-Heredia, T. Maurouard, V. Zhurbenko, and J. H. Ardenkjær-Larsen. “Calibrating Double-Loop H-Field Probe Measurements of RF Coil Current for MRI”. In: IEEE Journal of Electromagnetics, RF and Microwaves in Medicine and Biology 7 (3 Sept. 2023), pp. 266–272. ISSN: 2469-7249. DOI:10.1109/JERM.2023.3274742. 
   - [Accepted version (free)](https://orbit.dtu.dk/files/323172640/JERM_2022_12_0147.pdf); 
   - [Printed version (requires subscription)](https://doi.org/10.1109/JERM.2023.3274742).

# License

---------

# 前放大器釋耦暨阻抗匹配網絡計算器（漢語）
作者：王文俊

> 臣聞以德和民，不聞以亂。以亂，猶治絲而棼之也。——《左傳・隱公四年》（公元前719年）

諸markdown文件之在此GitHub庫者非皆有漢譯也。苟漢、英所述相異，以英文版為準。

此庫所圖者，
- 計算**三元件與四元件阻抗匹配網絡**【impedance matching network】也。可以呈高、低輸入阻抗，俾抑制電流于線圈，亦可以製前放大器之有低輸入阻抗者，此一也；
- 計算夫**前放大器釋耦、增益之與雜訊係數相權**也。可以擇工作點之合宜，俾前放大器釋耦【preamplifier decoupling】、增益與雜訊係數【noise figure】相均則，此又一也。

所實施者，算式、算法之列乎文獻\[1\]也。夫文獻\[1\]之所言，前放大器釋耦與雜訊係數之相權也；雖然，施諸放大器增益與雜訊係數之相權，俾計算之，亦可也。試參[理論之章](./docs/Theory.md)。

三元件、四元件網絡計算器有網頁版在[DTU RF Toolbox](https://rftoolbox.dtu.dk/rfcalc/NoiseMatching.html)。

## 安裝
1. 安裝[Python](https://www.python.org/)（至少3.11）、[Git](https://git-scm.com/)。
2. 執行下列於命令行，一步一行： <br/>
```powershell
git clone https://github.com/wenjunhj/impedance-matching-and-preamplifier-decoupling
# Alternatively, download the GitHub repository directly into any folder.
cd ./impedance-matching-and-preamplifier-decoupling
pip install -r requirements.txt
```
## 基本之用
有Jupyter簿三在`.\examples`之下：
- `three_element_network.ipynb`者，所以計算三元件前放大器釋耦暨匹配網絡也。
- `four_element_network.ipynb`者，所以計算四元件前放大器釋耦暨匹配網絡也。
- `preamplifier_decoupling_and_gain_vs_noise_figure.ipynb`，所以計算前放大器釋耦之與雜訊係數相權，抑放大器增益之與雜訊係數相權也。

之三簿調用函數於`amplifier.py`、`conversion.py`、`matching_decoupling_network.py`。


## 目錄
- [縮寫、語彙](#縮寫語彙)
- [感磁雙環之校準](#感磁雙環之校準)
- [詳用](./docs/Usage.md)
	- [三、四元件匹配網絡之予高、低阻抗者](./docs/Usage.md#three--and-four-element-matching-networks-for-high-or-low-impedance)
	- [前放大器釋耦、增益與雜訊係數之相權](./docs/Usage.md#preamplifier-decouplinggain-vs-noise-figure-trade-off)
- [駝峰響應之別註](./docs/Special_Notes_on_Camel-Hump_Responses.md)
- [實作](./docs/Practicalities.md)
- [理論](./docs/Theory.md)
- [雜記](#雜記)
- [參攷文獻](#參攷文獻)

## 縮寫、語彙

| 縮寫 | 意義                      |
| ------- | ---------------------------- |
| DC      | 直流【direct current】               |
| DF      | 耗損係數【dissipation factor】           |
| ESR     | 等效串聯電阻【equivalent series resistance】 |
| MR      | 磁共振【magnetic resonance】           |
| MRI     | 磁共振成像【magnetic resonance imaging】   |
| PCB     | 印製電路版【printed circuit board】        |
| Q       | 品質因數【quality factor】               |
| SNR     | 信號雜訊比【signal-to-noise ratio】       |
| SWR     | 駐波比【standing wave ratio】          |
| VNA     | 矢量網絡分析儀【vector network analyzer】      |

於此GitHub庫也，夫「匹配」、「阻抗匹配」、「阻抗變換」者，替易以用；夫「前放大器」、「放大器」者，替易以用。


## 感磁雙環之校準
薦此校正感磁雙環【double-loop H-field probe】之技以實測前放大器釋耦：
- 連雙環於矢量網絡分析儀【VNA】。凡有連接，緊之；凡須用力矩扳手【torque wrench】，用之。固雙環與纜之位，於測量過程之中，保夫雙環與纜安其所而不移。
- 出線圈（環天線）。以複數誌 $S_{21}$ 測量結果為 $S_{21,a}$ 。
- 復納線圈（環天線）。以複數誌 $S_{21}$ 測量結果為 $S_{21,b}$ 。
- 作複數減 $S_{21,\mathrm{cal}}=S_{21,b}-S_{21,a}$ 。

此技可校環間餘耦，廣其動態範圍。亦有
```math
S_{21,\mathrm{cal}} \approx \mathrm{j} \omega \kappa \mathrm{e}^{\mathrm{j} \omega \tau} \cdot I_\mathrm{loop}\text{，}
```
其中 $I_\mathrm{loop}$ 為綫圈之電流， $\kappa<0$ 、 $\tau<0$ 為常數之關乎器備者也，無須知之。猶欲詳知之，試閱文獻\[2\]。

## 詳用
[覿此](./docs/Usage.md)。

## 駝峰響應之別註
[覿此](./docs/Special_Notes_on_Camel-Hump_Responses.md)。

## 實作
[覿此](./docs/Practicalities.md)。

## 理論
[覿此](./docs/Theory.md)。

## 雜記
相關資助:
- Danmarks Grundforskningsfond (Danish National Research Foundation), DNRF-124
- European Research Council (ERC) Synergy grant 856432—HyperQ
- Innovation Fund Denmark grant E2409

## 參攷文獻
欲見羣參攷文獻，往[參攷文獻主表](./docs/References.md)。

1. W. Wang, V. Zhurbenko, J. D. Sánchez-Heredia, and J. H. Ardenkjær-Larsen. “Trade-off between preamplifier noise figure and decoupling in MRI detectors”. In: Magnetic Resonance in Medicine 89 (2 Feb. 2023), pp. 859–871. ISSN: 15222594. DOI: 10.1002/mrm.29489. 
   - [Open Access](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.29489)
2. W. Wang, J. D. Sánchez-Heredia, T. Maurouard, V. Zhurbenko, and J. H. Ardenkjær-Larsen. “Calibrating Double-Loop H-Field Probe Measurements of RF Coil Current for MRI”. In: IEEE Journal of Electromagnetics, RF and Microwaves in Medicine and Biology 7 (3 Sept. 2023), pp. 266–272. ISSN: 2469-7249. DOI:10.1109/JERM.2023.3274742. 
   - [接收版（免費）](https://orbit.dtu.dk/files/323172640/JERM_2022_12_0147.pdf)
   - [印製版（需資）](https://doi.org/10.1109/JERM.2023.3274742)
