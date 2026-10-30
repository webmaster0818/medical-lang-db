# 画面の文言 v2（変更した行だけ）

- v1 への saburo-2・taro-2 の指摘を反映。2台とも OK だった行は v1 のまま採用済み
- 判定の対象はこの表の行だけです。「OK」か「修正案＋理由」で返してください

## 英語原文の変更（訳はこれに合わせています）

- 4段階をデータに合わせた（tier C の施設は全件が翻訳機あり＝実データで確認済み。◎の根拠は「受入可能」の報告か医療通訳者・コーディネーターで、職員か通訳かはデータに無い）
  - A: Staff or interpreter → **Accepts this language** ／ 説明＝受入可能と報告、またはこの言語の医療通訳者・コーディネーターがいる
  - B: 説明を「この言語は電話・ビデオ通訳サービスで対応」に
  - C: 説明＝**翻訳機があり、この言語は翻訳機で対応**（「または要相談」を削除）
  - D: Ask before visiting → **Contact before visiting**（相談＝consult をやめ「連絡」に）
- 119: **Emergency in Japan**: call 119 (the ambulance is free; treatment is not)
- 見出し: English-speaking … → **… with English support**（△―も含む一覧のため）
- listedFirst: 「職員・通訳者がいる施設が先」→「対応度の高い順（◎から）」

## ko（14行）

| key | v1 | v2 |
|---|---|---|
| tierA | 직원 또는 통역사 | 이 언어로 진료 가능 |
| tierAdesc | 이 의료기관은 이 언어로 진료할 수 있다고 보고했습니다. | 이 언어로 환자를 진료할 수 있다고 의료기관이 보고했거나, 이 언어의 의료 통역사·코디네이터가 있습니다. |
| tierBdesc | 원격 통역 서비스를 통해 지원합니다. | 이 언어는 전화·화상 통역 서비스로 지원합니다. |
| tierCdesc | 번역기로 지원하거나, 방문 전 상담을 요청합니다. | 번역기가 있으며, 이 언어는 번역기로 지원합니다. |
| tierDdesc | 이 언어가 등록되어 있지만, 방문 전 상담이 필요하며 번역기는 없습니다. | 이 언어가 등록되어 있지만, 방문 전에 의료기관에 문의해야 하며 번역기는 없습니다. |
| languages | 대응 언어 | 지원 언어 |
| emergency | 응급 시: 119에 전화(구급차, 무료) | 일본에서 응급 시: 119에 전화(구급차 이용은 무료, 치료비는 유료) |
| holidays | 공휴일 = 일본의 국경일 | 공휴일 = 일본의 법정 공휴일 |
| listedFirst | 직원 또는 통역사가 있는 의료기관을 먼저 표시합니다. | 지원 수준이 높은 순(◎부터)으로 표시합니다. |
| cityH1 | {place}의 한국어 진료 가능 병원·의원 | {place}의 한국어 지원 병원·의원 |
| cityTitle | {place}의 한국어 진료 가능 병원·의원 ({n}곳) | {place}의 한국어 지원 병원·의원 ({n}곳) |
| deptH1 | {place}의 한국어 진료 가능 {dept} | {place}의 한국어 지원 {dept} |
| deptTitle | {place}의 한국어 진료 가능 {dept} ({n}곳) | {place}의 한국어 지원 {dept} ({n}곳) |
| clinicTitle | {name} – 한국어 대응·진료 시간·전화번호 | {name} – 한국어 지원·진료 시간·전화번호 |

## zh-hant（17行）

| key | v1 | v2 |
|---|---|---|
| tierA | 職員或口譯員 | 可用此語言看診 |
| tierAdesc | 該醫療機構申報可用此語言看診。 | 醫療機構表示可用此語言看診，或備有此語言的醫療口譯員或協調員。 |
| tierBdesc | 透過遠端口譯服務提供協助。 | 此語言透過電話或視訊口譯服務提供協助。 |
| tierCdesc | 以翻譯機協助，或要求就診前先諮詢。 | 備有翻譯機，此語言以翻譯機協助。 |
| tierDdesc | 已登記此語言，但需就診前先諮詢，且未備有翻譯機。 | 已登記此語言，但需就診前先洽詢醫療機構，且未備有翻譯機。 |
| hol | 假日 | 國定假日 |
| languages | 對應語言 | 支援語言 |
| emergency | 緊急時請撥119（救護車，免費） | 在日本緊急時請撥119叫救護車（救護車免費，醫療費需自付） |
| holidays | 假日＝日本國定假日 | 國定假日＝日本的國定假日 |
| listedFirst | 有職員或口譯員的醫療機構優先列出。 | 依支援等級由高至低排列（◎優先）。 |
| srcD5 | 外國患者受理醫療機構名單（厚生勞動省） | 接受外國患者的醫療機構名單（厚生勞動省） |
| cityH1 | {place}可用中文就診的醫院與診所 | {place}提供中文支援的醫院與診所 |
| cityTitle | {place}可用中文就診的醫院與診所（{n}家） | {place}提供中文支援的醫院與診所（{n}家） |
| cityDesc | {place}登記可用中文（含台語、粵語）的醫院、診所與牙醫診所共{n}家，附看診時間、是否需預約及電話。 | {place}登記可用中文的醫院、診所與牙醫診所共{n}家，附看診時間、是否需預約及電話。 |
| deptH1 | {place}可用中文就診的{dept} | {place}提供中文支援的{dept} |
| deptTitle | {place}可用中文就診的{dept}（{n}家） | {place}提供中文支援的{dept}（{n}家） |
| clinicTitle | {name}－中文對應、看診時間與電話 | {name}－中文支援、看診時間與電話 |

## zh-hans（20行）

| key | v1 | v2 |
|---|---|---|
| tierA | 工作人员或翻译 | 可用此语言就诊 |
| tierAdesc | 该医疗机构申报可用此语言就诊。 | 医疗机构表示可用此语言就诊，或配有此语言的医疗口译员或协调员。 |
| tierB | 电话或视频翻译 | 电话或视频口译 |
| tierBdesc | 通过远程翻译服务提供协助。 | 此语言通过电话或视频口译服务提供协助。 |
| tierC | 翻译设备 | 翻译机 |
| tierCdesc | 借助翻译设备提供协助，或要求就诊前先咨询。 | 备有翻译机，此语言借助翻译机提供协助。 |
| tierD | 就诊前请先咨询 | 就诊前请先联系 |
| tierDdesc | 已登记此语言，但需就诊前先咨询，且没有翻译设备。 | 已登记此语言，但需就诊前先联系医疗机构，且没有翻译机。 |
| hol | 节假日 | 法定节假日 |
| departments | 科室与接诊时间 | 科室与门诊时间 |
| translationDevice | 备有翻译设备 | 备有翻译机 |
| languages | 对应语言 | 支持语言 |
| emergency | 紧急情况请拨打119（救护车，免费） | 在日本，紧急情况请拨打119叫救护车（救护车免费，治疗费用需自付） |
| holidays | 节假日＝日本法定节假日 | 法定节假日＝日本的法定节假日 |
| listedFirst | 有工作人员或翻译的医疗机构排在前面。 | 按支持等级从高到低排列（◎在前）。 |
| srcD5 | 外国患者接收医疗机构名单（厚生劳动省） | 接收外国患者的医疗机构名单（厚生劳动省） |
| cityH1 | {place}可用中文就诊的医院和诊所 | {place}提供中文支持的医院和诊所 |
| cityTitle | {place}可用中文就诊的医院和诊所（{n}家） | {place}提供中文支持的医院和诊所（{n}家） |
| deptH1 | {place}可用中文就诊的{dept} | {place}提供中文支持的{dept} |
| deptTitle | {place}可用中文就诊的{dept}（{n}家） | {place}提供中文支持的{dept}（{n}家） |

## vi（15行）

| key | v1 | v2 |
|---|---|---|
| tierA | Nhân viên hoặc phiên dịch viên | Có thể khám bằng ngôn ngữ này |
| tierAdesc | Cơ sở y tế cho biết có thể khám cho bệnh nhân bằng ngôn ngữ này. | Cơ sở cho biết có thể khám bằng ngôn ngữ này, hoặc có phiên dịch viên hay điều phối viên y tế cho ngôn ngữ này. |
| tierBdesc | Hỗ trợ thông qua dịch vụ phiên dịch từ xa. | Ngôn ngữ này được hỗ trợ qua dịch vụ phiên dịch bằng điện thoại hoặc video. |
| tierCdesc | Hỗ trợ bằng máy phiên dịch, hoặc cơ sở yêu cầu liên hệ trao đổi trước. | Cơ sở có máy phiên dịch và dùng máy cho ngôn ngữ này. |
| tierD | Hỏi trước khi đến | Liên hệ trước khi đến |
| tierDdesc | Ngôn ngữ này có được đăng ký, nhưng cơ sở yêu cầu liên hệ trao đổi trước và không có máy phiên dịch. | Ngôn ngữ này có được đăng ký, nhưng cơ sở yêu cầu liên hệ trước và không có máy phiên dịch. |
| departments | Khoa khám và giờ khám | Chuyên khoa và giờ khám |
| payments | Thẻ và tiền điện tử | Thẻ và thanh toán điện tử |
| cashOnly | Không có thông tin về thẻ hoặc tiền điện tử | Không có thông tin về thẻ hoặc thanh toán điện tử |
| emergency | Cấp cứu: gọi 119 (xe cứu thương, miễn phí) | Cấp cứu tại Nhật Bản: gọi 119 (xe cứu thương miễn phí, chi phí điều trị phải tự trả) |
| listedFirst | Cơ sở có nhân viên hoặc phiên dịch viên được liệt kê trước. | Sắp xếp theo mức hỗ trợ từ cao đến thấp (◎ trước). |
| cityH1 | Bệnh viện và phòng khám nói tiếng Việt tại {place} | Bệnh viện và phòng khám có hỗ trợ tiếng Việt tại {place} |
| cityTitle | Bệnh viện và phòng khám nói tiếng Việt tại {place} ({n}) | Bệnh viện và phòng khám có hỗ trợ tiếng Việt tại {place} ({n}) |
| deptH1 | {dept} nói tiếng Việt tại {place} | {dept} có hỗ trợ tiếng Việt tại {place} |
| deptTitle | {dept} nói tiếng Việt tại {place} ({n}) | {dept} có hỗ trợ tiếng Việt tại {place} ({n}) |

## pt（14行）

| key | v1 | v2 |
|---|---|---|
| tierA | Funcionário ou intérprete | Atende neste idioma |
| tierAdesc | A instituição informa que pode atender pacientes neste idioma. | A instituição informa que atende pacientes neste idioma, ou tem intérprete ou coordenador médico para ele. |
| tierBdesc | O atendimento é feito por um serviço de interpretação remota. | O atendimento neste idioma é feito por intérprete por telefone ou vídeo. |
| tierCdesc | O atendimento depende de um aparelho de tradução, ou a instituição pede consulta prévia. | A instituição tem aparelho de tradução e o utiliza para este idioma. |
| tierD | Consulte antes de ir | Entre em contato antes de ir |
| tierDdesc | O idioma está registrado, mas a instituição pede consulta prévia e não tem aparelho de tradução. | O idioma está registrado, mas a instituição pede que você entre em contato antes e não tem aparelho de tradução. |
| payments | Cartões e dinheiro eletrônico | Cartões e pagamentos eletrônicos |
| cashOnly | Nenhum cartão ou dinheiro eletrônico informado | Nenhum cartão ou pagamento eletrônico informado |
| emergency | Emergência: ligue 119 (ambulância, gratuita) | Emergência no Japão: ligue 119 (a ambulância é gratuita; o tratamento é pago) |
| listedFirst | Instituições com funcionários ou intérpretes aparecem primeiro. | Listadas do maior para o menor nível de atendimento (◎ primeiro). |
| cityH1 | Hospitais e clínicas que atendem em português em {place} | Hospitais e clínicas em {place} com atendimento em português |
| cityTitle | Hospitais e clínicas que atendem em português em {place} ({n}) | Hospitais e clínicas em {place} com atendimento em português ({n}) |
| deptH1 | {dept} com atendimento em português em {place} | {dept} em {place} com atendimento em português |
| deptTitle | {dept} com atendimento em português em {place} ({n}) | {dept} em {place} com atendimento em português ({n}) |
