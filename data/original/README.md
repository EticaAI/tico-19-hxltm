# data/original

> TODO: document it better

<details>
<summary>Code to generate this directory</summary>

```bash
# generate data-original/
./scripts/data-original-download.sh
./scripts/data-original-prepare.sh
```

</details>

## Original content

Note: original is downloaded from <https://github.com/tico-19/tico-19.github.io>
and is not committed on this repository, but can be generated _as it is_ using
the script [scripts/data-original-prepare.sh](../../scripts/data-original-prepare.sh):

- paper/
- terminologies/
- TM/
- fb_covid-19.zip
- google_covid-19.zip
- tico19-testset.zip

---

Click to see full list on non-committed files you would see if run the
scripts:


<details>
<summary>tree data/original</summary>

```txt
tree
.
├── fb_covid-19.zip
├── google_covid-19.zip
├── paper
│   ├── ticopaper.bib
│   └── ticopaper.pdf
├── README.md
├── terminologies
│   ├── f_en-af_ZA.csv
│   ├── f_en-am_ET.csv
│   ├── f_en-ar_AR.csv
│   ├── f_en-as_IN.csv
│   ├── f_en-az_AZ.csv
│   ├── f_en-be_BY.csv
│   ├── f_en-bg_BG.csv
│   ├── f_en-bn_IN.csv
│   ├── f_en-bs_BA.csv
│   ├── f_en-ca_ES.csv
│   ├── f_en-cb_IQ.csv
│   ├── f_en-cs_CZ.csv
│   ├── f_en-cx_PH.csv
│   ├── f_en-da_DK.csv
│   ├── f_en-de_DE.csv
│   ├── f_en-el_GR.csv
│   ├── f_en-es_XX.csv
│   ├── f_en-et_EE.csv
│   ├── f_en-fa_IR.csv
│   ├── f_en-fi_FI.csv
│   ├── f_en-fr_XX.csv
│   ├── f_en-gu_IN.csv
│   ├── f_en-ha_NG.csv
│   ├── f_en-he_IL.csv
│   ├── f_en-hi_IN.csv
│   ├── f_en-hr_HR.csv
│   ├── f_en-ht_HT.csv
│   ├── f_en-hu_HU.csv
│   ├── f_en-hy_AM.csv
│   ├── f_en-id_ID.csv
│   ├── f_en-ig_NG.csv
│   ├── f_en-is_IS.csv
│   ├── f_en-it_IT.csv
│   ├── f_en-ja_XX.csv
│   ├── f_en-jv_ID.csv
│   ├── f_en-ka_GE.csv
│   ├── f_en-kk_KZ.csv
│   ├── f_en-km_KH.csv
│   ├── f_en-kn_IN.csv
│   ├── f_en-ko_KR.csv
│   ├── f_en-lg_UG.csv
│   ├── f_en-ln_CD.csv
│   ├── f_en-lo_LA.csv
│   ├── f_en-lt_LT.csv
│   ├── f_en-lv_LV.csv
│   ├── f_en-mg_MG.csv
│   ├── f_en-mk_MK.csv
│   ├── f_en-ml_IN.csv
│   ├── f_en-mn_MN.csv
│   ├── f_en-mr_IN.csv
│   ├── f_en-ms_MY.csv
│   ├── f_en-my_MM.csv
│   ├── f_en-ne_NP.csv
│   ├── f_en-nl_XX.csv
│   ├── f_en-no_XX.csv
│   ├── f_en-ns_ZA.csv
│   ├── f_en-om_KE.csv
│   ├── f_en-pa_IN.csv
│   ├── f_en-pl_PL.csv
│   ├── f_en-ps_AF.csv
│   ├── f_en-pt_XX.csv
│   ├── f_en-ro_RO.csv
│   ├── f_en-ru_RU.csv
│   ├── f_en-si_LK.csv
│   ├── f_en-sk_SK.csv
│   ├── f_en-sl_SI.csv
│   ├── f_en-so_SO.csv
│   ├── f_en-sq_AL.csv
│   ├── f_en-sr_RS.csv
│   ├── f_en-ss_SZ.csv
│   ├── f_en-su_ID.csv
│   ├── f_en-sv_SE.csv
│   ├── f_en-sw_KE.csv
│   ├── f_en-ta_IN.csv
│   ├── f_en-te_IN.csv
│   ├── f_en-th_TH.csv
│   ├── f_en-tl_XX.csv
│   ├── f_en-tn_BW.csv
│   ├── f_en-tr_TR.csv
│   ├── f_en-uk_UA.csv
│   ├── f_en-ur_PK.csv
│   ├── f_en-vi_VN.csv
│   ├── f_en-wo_SN.csv
│   ├── f_en-xh_ZA.csv
│   ├── f_en-yo_NG.csv
│   ├── f_en-zh_CN.csv
│   ├── f_en-zh_TW.csv
│   ├── f_en-zu_ZA.csv
│   ├── g_ar_en.csv
│   ├── g_bn_en.csv
│   ├── g_cs_en.csv
│   ├── g_da_en.csv
│   ├── g_de_en.csv
│   ├── g_en_af.csv
│   ├── g_en_am.csv
│   ├── g_en_ar.csv
│   ├── g_en_az.csv
│   ├── g_en_be.csv
│   ├── g_en_bg.csv
│   ├── g_en_bn.csv
│   ├── g_en_bs.csv
│   ├── g_en_ca.csv
│   ├── g_en_ceb.csv
│   ├── g_en_co.csv
│   ├── g_en_cs.csv
│   ├── g_en_cy.csv
│   ├── g_en_da.csv
│   ├── g_en_de.csv
│   ├── g_en_el.csv
│   ├── g_en_eo.csv
│   ├── g_en_es-419.csv
│   ├── g_en_et.csv
│   ├── g_en_eu.csv
│   ├── g_en_fa.csv
│   ├── g_en_fi.csv
│   ├── g_en_fil.csv
│   ├── g_en_fr-FR.csv
│   ├── g_en_fy.csv
│   ├── g_en_ga.csv
│   ├── g_en_gd.csv
│   ├── g_en_gl.csv
│   ├── g_en_gu.csv
│   ├── g_en_ha.csv
│   ├── g_en_he.csv
│   ├── g_en_hi.csv
│   ├── g_en_hmn.csv
│   ├── g_en_hr.csv
│   ├── g_en_ht.csv
│   ├── g_en_hu.csv
│   ├── g_en_hy.csv
│   ├── g_en_id.csv
│   ├── g_en_ig.csv
│   ├── g_en_is.csv
│   ├── g_en_it.csv
│   ├── g_en_ja.csv
│   ├── g_en_jv.csv
│   ├── g_en_ka.csv
│   ├── g_en_kk.csv
│   ├── g_en_km.csv
│   ├── g_en_kn.csv
│   ├── g_en_ko.csv
│   ├── g_en_ku.csv
│   ├── g_en_ky.csv
│   ├── g_en_la.csv
│   ├── g_en_lb.csv
│   ├── g_en_lo.csv
│   ├── g_en_lt.csv
│   ├── g_en_lv.csv
│   ├── g_en_mg.csv
│   ├── g_en_mk.csv
│   ├── g_en_ml.csv
│   ├── g_en_mn.csv
│   ├── g_en_mr.csv
│   ├── g_en_ms.csv
│   ├── g_en_my.csv
│   ├── g_en_nb.csv
│   ├── g_en_ne.csv
│   ├── g_en_nl.csv
│   ├── g_en_ny.csv
│   ├── g_en_pa.csv
│   ├── g_en_pl.csv
│   ├── g_en_ps.csv
│   ├── g_en_pt-BR.csv
│   ├── g_en_ro.csv
│   ├── g_en_ru.csv
│   ├── g_en_sd.csv
│   ├── g_en_si.csv
│   ├── g_en_sk.csv
│   ├── g_en_sl.csv
│   ├── g_en_sm.csv
│   ├── g_en_sn.csv
│   ├── g_en_so.csv
│   ├── g_en_sq.csv
│   ├── g_en_sr.csv
│   ├── g_en_st.csv
│   ├── g_en_su.csv
│   ├── g_en_sv.csv
│   ├── g_en_sw.csv
│   ├── g_en_ta.csv
│   ├── g_en_te.csv
│   ├── g_en_tg.csv
│   ├── g_en_th.csv
│   ├── g_en_tr.csv
│   ├── g_en_uk.csv
│   ├── g_en_ur.csv
│   ├── g_en_uz.csv
│   ├── g_en_vi.csv
│   ├── g_en_xh.csv
│   ├── g_en_yi.csv
│   ├── g_en_yo.csv
│   ├── g_en_zh-CN.csv
│   ├── g_en_zh-TW.csv
│   ├── g_en_zu.csv
│   ├── g_es-419_en.csv
│   ├── g_es-ES_en.csv
│   ├── g_fa_en.csv
│   ├── g_fr_en.csv
│   ├── g_hi_en.csv
│   ├── g_id_en.csv
│   ├── g_it_en.csv
│   ├── g_iw_en.csv
│   ├── g_ja_en.csv
│   ├── g_ko_en.csv
│   ├── g_ms_en.csv
│   ├── g_nl_en.csv
│   ├── g_no_en.csv
│   ├── g_pt-BR_en.csv
│   ├── g_pt-PT_en.csv
│   ├── g_ru_en.csv
│   ├── g_sv_en.csv
│   ├── g_th_en.csv
│   ├── g_tr_en.csv
│   ├── g_vi_en.csv
│   ├── g_zh-CN_en.csv
│   └── g_zh-TW_en.csv
├── terminologies.zip
├── tico19-testset.zip
└── TM
    ├── all.am-om.tmx.zip
    ├── all.am-ti.tmx.zip
    ├── all.ar-es-LA.tmx.zip
    ├── all.ar-fr.tmx.zip
    ├── all.ar-hi.tmx.zip
    ├── all.ar-id.tmx.zip
    ├── all.ar-pt-BR.tmx.zip
    ├── all.ar-ru.tmx.zip
    ├── all.ar-zh.tmx.zip
    ├── all.en-ar.tmx.zip
    ├── all.en-bn.tmx.zip
    ├── all.en-ckb.tmx
    ├── all.en_ckb.tmx
    ├── all.en-ckb.tmx.zip
    ├── all.en_ckb.tmx.zip
    ├── all.en-din.tmx.zip
    ├── all.en-es-419.tmx
    ├── all.en-es-LA.tmx.zip
    ├── all.en-fa.old.tmx.zip
    ├── all.en-fa.tmx.zip
    ├── all.en-fr.tmx
    ├── all.en-fr.tmx.zip
    ├── all.en-fuv.tmx
    ├── all.en-fuv.tmx.zip
    ├── all.en-ha.tmx.zip
    ├── all.en-hi.tmx
    ├── all.en-hi.tmx.zip
    ├── all.en-id.tmx
    ├── all.en-id.tmx.zip
    ├── all.en-km.tmx.zip
    ├── all.en-kr.tmx.zip
    ├── all.en-ku.tmx
    ├── all.en-ku.tmx.zip
    ├── all.en-lg.tmx
    ├── all.en-lg.tmx.zip
    ├── all.en-ln.tmx
    ├── all.en-ln.tmx.zip
    ├── all.en-mr.tmx.zip
    ├── all.en-ms.tmx
    ├── all.en-ms.tmx.zip
    ├── all.en-my.tmx.zip
    ├── all.en-ne.tmx.zip
    ├── all.en-nus.tmx.zip
    ├── all.en-om.tmx.zip
    ├── all.en-prs.tmx.zip
    ├── all.en-ps.tmx
    ├── all.en-ps.tmx.zip
    ├── all.en-pt-BR.tmx
    ├── all.en-pt-BR.tmx.zip
    ├── all.en-ru.tmx
    ├── all.en-ru.tmx.zip
    ├── all.en-rw.tmx
    ├── all.en-rw.tmx.zip
    ├── all.en-so.tmx.zip
    ├── all.en-sw.tmx.zip
    ├── all.en-ta.tmx.zip
    ├── all.en-ti_ER.tmx.zip
    ├── all.en-ti_ET.tmx.zip
    ├── all.en-ti.tmx.zip
    ├── all.en-tl.tmx.zip
    ├── all.en-ur.tmx
    ├── all.en-ur.tmx.zip
    ├── all.en-zh.tmx
    ├── all.en-zh.tmx.zip
    ├── all.en-zu.tmx.zip
    ├── all.es-LA-ar.tmx.zip
    ├── all.es-LA-fr.tmx.zip
    ├── all.es-LA-hi.tmx.zip
    ├── all.es-LA-id.tmx.zip
    ├── all.es-LA-pt-BR.tmx.zip
    ├── all.es-LA-ru.tmx.zip
    ├── all.es-LA-zh.tmx.zip
    ├── all.fa-prs.tmx.zip
    ├── all.fr-ar.tmx.zip
    ├── all.fr-es-LA.tmx.zip
    ├── all.fr-fuv.tmx.zip
    ├── all.fr-hi.tmx.zip
    ├── all.fr-id.tmx.zip
    ├── all.fr-lg.tmx.zip
    ├── all.fr-ln.tmx.zip
    ├── all.fr-pt-BR.tmx.zip
    ├── all.fr-ru.tmx.zip
    ├── all.fr-rw.tmx.zip
    ├── all.fr-sw.tmx.zip
    ├── all.fr-zh.tmx.zip
    ├── all.fr-zu.tmx.zip
    ├── all.hi-ar.tmx.zip
    ├── all.hi-bn.tmx.zip
    ├── all.hi-es-LA.tmx.zip
    ├── all.hi-fr.tmx.zip
    ├── all.hi-id.tmx.zip
    ├── all.hi-mr.tmx.zip
    ├── all.hi-pt-BR.tmx.zip
    ├── all.hi-ru.tmx.zip
    ├── all.hi-ur.tmx.zip
    ├── all.hi-zh.tmx.zip
    ├── all.id-ar.tmx.zip
    ├── all.id-es-LA.tmx.zip
    ├── all.id-fr.tmx.zip
    ├── all.id-hi.tmx.zip
    ├── all.id-pt-BR.tmx.zip
    ├── all.id-ru.tmx.zip
    ├── all.id-zh.tmx.zip
    ├── all.ku-ckb.tmx.zip
    ├── all.pt-BR-ar.tmx.zip
    ├── all.pt-BR-es-LA.tmx.zip
    ├── all.pt-BR-fr.tmx.zip
    ├── all.pt-BR-hi.tmx.zip
    ├── all.pt-BR-id.tmx.zip
    ├── all.pt-BR-ru.tmx.zip
    ├── all.pt-BR-zh.tmx.zip
    ├── all.ru-ar.tmx.zip
    ├── all.ru-es-LA.tmx.zip
    ├── all.ru-fr.tmx.zip
    ├── all.ru-hi.tmx.zip
    ├── all.ru-id.tmx.zip
    ├── all.ru-pt-BR.tmx.zip
    ├── all.ru-zh.tmx.zip
    ├── all.zh-ar.tmx.zip
    ├── all.zh-es-LA.tmx.zip
    ├── all.zh-fr.tmx.zip
    ├── all.zh-hi.tmx.zip
    ├── all.zh-id.tmx.zip
    ├── all.zh-pt-BR.tmx.zip
    ├── all.zh-ru.tmx.zip
    ├── en-ckb.tmx.zip
    ├── en_ckb.tsv.tmx-2020-4-29_3-1.zip
    ├── en-es-419.tmx.zip
    ├── en_es.tsv.tmx-2020-4-29_2-57.zip
    ├── en-fr.tmx.zip
    ├── en-fuv.tmx.zip
    ├── en_fuv.tsv.tmx-2020-4-29_3-2.zip
    ├── en-hi.tmx.zip
    ├── en-id.tmx.zip
    ├── en-ku.tmx.zip
    ├── en-lg.tmx.zip
    ├── en-ln.tmx.zip
    ├── en_mr.tsv.tmx-2020-4-29_3-4.zip
    ├── en-ms.tmx.zip
    ├── en_ms.tsv.tmx-2020-4-29_3-7.zip
    ├── en-ps.tmx.zip
    ├── en-pt-BR.tmx.zip
    ├── en_pt-BR.tsv.tmx-2020-4-29_3-8.zip
    ├── en-ru.tmx.zip
    ├── en-rw.tmx.zip
    ├── en_so.tsv.tmx-2020-4-29_3-9.zip
    ├── en_sw.tsv.tmx-2020-4-29_3-9.zip
    ├── en-ur.tmx.zip
    ├── en_ur.tsv.tmx-2020-4-29_3-10.zip
    ├── en-zh.tmx.zip
    ├── en_zu.tsv.tmx-2020-4-29_3-10.zip
    └── README.md.zip

3 directories, 374 files

```
</details>

---

The committed files under `data/original` are generated with
[scripts/data-original-prepare.sh](../../scripts/data-original-prepare.sh) and
have changes also documented / justified on [CHANGELOG.md](../../CHANGELOG.md).
**Mostly they are data cleaning, formatting and some fixes (with explaination)
on how language codes used to label de terminology and translations.** This
is done as previous step to convert to HXLTM format.

### cat paper/ticopaper.bib
> Note: Emerson Rocha, from Etica.AI is not associated with the TICO-19 team.
> Even if you use this work, please consider citing the original lexicographers.

```bibtex
@misc{tico-19,
author={Anastasopoulos, Antonios and Cattelan, Alessandro and Dou, Zi-Yi and Federico, Marcello and Federmann, Christian and  Genzel, Dmitriy and Guzm\'{a}n, Francisco and Hu, Junjie and Hughes, Macduff and Koehn, Philipp and Lazar, Rosie and Lewis, Will and Neubig, Graham and Niu, Mengmeng and \"{O}ktem, Alp and Paquin, Eric and Tang, Grace and Tur, Sylwia},
title={{TICO}-19: the {T}ranslation Initiative for {CO}vid-19},
year={2020},
note={{arXiv}:2007.01788}
}
```
