# 画面の文言 訳の突き合わせ（v1・tomomi-2 訳）

- 元データ: `data/ui/strings.json`。英語は `lib/ui.ts`
- 地名・診療科・言語名・曜日（月〜日）はここに含まない（辞書・Unicode CLDR から自動）
- {place} {dept} {n} {name} は差し込み。zh-hant は中文・台語・粵語の利用者向け、pt はブラジル（pt-BR）向け

## ko

| key | 英語（原文） | 訳案 | 意図 |
|---|---|---|---|
| tagline | Hospitals and clinics in Japan that accept patients in your language | 한국어로 진료받을 수 있는 일본의 병원·의원 |  |
| tierA | Staff or interpreter | 직원 또는 통역사 | ◎ 職員・通訳者が対応 |
| tierAdesc | The facility reports it can see patients in this language. | 이 의료기관은 이 언어로 진료할 수 있다고 보고했습니다. |  |
| tierB | Phone or video interpreter | 전화·화상 통역 | ○ 電話・ビデオ通訳 |
| tierBdesc | Support is through a remote interpreting service. | 원격 통역 서비스를 통해 지원합니다. |  |
| tierC | Translation device | 번역기 | △ 翻訳機、または要相談 |
| tierCdesc | Support relies on a translation device, or the facility asks you to consult first. | 번역기로 지원하거나, 방문 전 상담을 요청합니다. |  |
| tierD | Ask before visiting | 방문 전 문의 | ― 要相談で翻訳機なし（受診前に問い合わせを） |
| tierDdesc | The language is listed, but the facility asks you to consult first and has no translation device. | 이 언어가 등록되어 있지만, 방문 전 상담이 필요하며 번역기는 없습니다. |  |
| hospital | Hospital | 병원 |  |
| clinic | Clinic | 의원 |  |
| dental | Dental clinic | 치과 |  |
| hol | Hol | 공휴일 | 表の見出し（短く） |
| openNow | Open now | 진료 중 |  |
| closedNow | Closed now | 진료 시간 외 |  |
| bookingRequired | Appointment required | 예약 필요 | ko/zh-hant は辞書（出典つき）の表現 |
| bookingNotRequired | Walk-ins accepted | 예약 없이 진료 가능 | ko/zh-hant は辞書（出典つき）の表現 |
| phone | Phone | 전화 |  |
| phoneForeign | Phone for foreign patients | 외국인 환자용 전화 |  |
| address | Address | 주소 |  |
| showDriver | Show this to a taxi driver | 택시 기사에게 보여 주세요 |  |
| departments | Departments and hours | 진료과와 진료 시간 |  |
| otherDepts | Other departments (Japanese names) | 기타 진료과(일본어 명칭) |  |
| payments | Cards and e-money | 신용카드·전자화폐 |  |
| cashOnly | No cards or e-money reported | 등록된 신용카드·전자화폐 없음 |  |
| translationDevice | Translation device available | 번역기 있음 |  |
| languages | Languages | 대응 언어 |  |
| sources | Sources | 출처 |  |
| lastUpdated | Last updated by the facility | 의료기관 최종 갱신일 |  |
| disclaimer | Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit. | 각 의료기관이 후생노동성에 보고한 정보입니다. 진료 시간과 언어 지원은 바뀔 수 있으니 방문 전에 전화로 확인해 주세요. |  |
| emergency | Emergency: call 119 (ambulance, free of charge) | 응급 시: 119에 전화(구급차, 무료) | 119番＝救急車（無料） |
| byDept | By department | 진료과별 |  |
| allFacilities | All facilities | 전체 의료기관 |  |
| website | Website | 웹사이트 |  |
| holidays | Hol = national holidays | 공휴일 = 일본의 국경일 |  |
| home | Home | 홈 |  |
| searchByArea | Search by area | 지역으로 찾기 |  |
| howToRead | How to read the language support levels | 언어 지원 수준 보는 법 |  |
| listedFirst | Facilities with staff or interpreters are listed first. | 직원 또는 통역사가 있는 의료기관을 먼저 표시합니다. |  |
| srcMhlwNet | Medical Information Net (Ministry of Health, Labour and Welfare) | 의료정보넷(医療情報ネット, 후생노동성) | 公式名「医療情報ネット」を併記 |
| srcD5 | List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare) | 외국인 환자를 받는 의료기관 목록(후생노동성) |  |
| count | {n} facilities | {n}곳 | 施設数の表示 |
| cityH1 | English-speaking hospitals and clinics in {place} | {place}의 한국어 진료 가능 병원·의원 |  |
| cityTitle | English-speaking hospitals and clinics in {place} ({n}) | {place}의 한국어 진료 가능 병원·의원 ({n}곳) |  |
| cityDesc | {n} hospitals, clinics and dental clinics in {place} that list English support, with hours, appointment rules and phone numbers. | {place}에서 한국어 대응을 등록한 병원·의원·치과 {n}곳. 진료 시간, 예약 여부, 전화번호를 확인할 수 있습니다. | 検索結果の説明文 |
| deptH1 | English-speaking {dept} in {place} | {place}의 한국어 진료 가능 {dept} |  |
| deptTitle | English-speaking {dept} in {place} ({n}) | {place}의 한국어 진료 가능 {dept} ({n}곳) |  |
| clinicTitle | {name} – English support, hours and phone | {name} – 한국어 대응·진료 시간·전화번호 |  |

## zh-hant

| key | 英語（原文） | 訳案 | 意図 |
|---|---|---|---|
| tagline | Hospitals and clinics in Japan that accept patients in your language | 在日本可用中文就診的醫院與診所 |  |
| tierA | Staff or interpreter | 職員或口譯員 | ◎ 職員・通訳者が対応 |
| tierAdesc | The facility reports it can see patients in this language. | 該醫療機構申報可用此語言看診。 |  |
| tierB | Phone or video interpreter | 電話或視訊口譯 | ○ 電話・ビデオ通訳 |
| tierBdesc | Support is through a remote interpreting service. | 透過遠端口譯服務提供協助。 |  |
| tierC | Translation device | 翻譯機 | △ 翻訳機、または要相談 |
| tierCdesc | Support relies on a translation device, or the facility asks you to consult first. | 以翻譯機協助，或要求就診前先諮詢。 |  |
| tierD | Ask before visiting | 就診前請先洽詢 | ― 要相談で翻訳機なし（受診前に問い合わせを） |
| tierDdesc | The language is listed, but the facility asks you to consult first and has no translation device. | 已登記此語言，但需就診前先諮詢，且未備有翻譯機。 |  |
| hospital | Hospital | 醫院 |  |
| clinic | Clinic | 診所 |  |
| dental | Dental clinic | 牙醫診所 |  |
| hol | Hol | 假日 | 表の見出し（短く） |
| openNow | Open now | 看診中 |  |
| closedNow | Closed now | 非看診時間 |  |
| bookingRequired | Appointment required | 必須預約 | ko/zh-hant は辞書（出典つき）の表現 |
| bookingNotRequired | Walk-ins accepted | 無須預約即可看診 | ko/zh-hant は辞書（出典つき）の表現 |
| phone | Phone | 電話 |  |
| phoneForeign | Phone for foreign patients | 外國患者專用電話 |  |
| address | Address | 地址 |  |
| showDriver | Show this to a taxi driver | 請出示給計程車司機 |  |
| departments | Departments and hours | 科別與看診時間 |  |
| otherDepts | Other departments (Japanese names) | 其他科別（日文名稱） |  |
| payments | Cards and e-money | 信用卡與電子支付 |  |
| cashOnly | No cards or e-money reported | 未登記可用的信用卡或電子支付 |  |
| translationDevice | Translation device available | 備有翻譯機 |  |
| languages | Languages | 對應語言 |  |
| sources | Sources | 資料來源 |  |
| lastUpdated | Last updated by the facility | 醫療機構最後更新日 |  |
| disclaimer | Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit. | 資料由各醫療機構向厚生勞動省申報。看診時間與語言支援可能變動，就診前請先致電確認。 |  |
| emergency | Emergency: call 119 (ambulance, free of charge) | 緊急時請撥119（救護車，免費） | 119番＝救急車（無料） |
| byDept | By department | 依科別 |  |
| allFacilities | All facilities | 所有醫療機構 |  |
| website | Website | 網站 |  |
| holidays | Hol = national holidays | 假日＝日本國定假日 |  |
| home | Home | 首頁 |  |
| searchByArea | Search by area | 依地區搜尋 |  |
| howToRead | How to read the language support levels | 語言支援等級說明 |  |
| listedFirst | Facilities with staff or interpreters are listed first. | 有職員或口譯員的醫療機構優先列出。 |  |
| srcMhlwNet | Medical Information Net (Ministry of Health, Labour and Welfare) | 醫療資訊網（医療情報ネット・厚生勞動省） | 公式名「医療情報ネット」を併記 |
| srcD5 | List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare) | 外國患者受理醫療機構名單（厚生勞動省） |  |
| count | {n} facilities | {n}家 | 施設数の表示 |
| cityH1 | English-speaking hospitals and clinics in {place} | {place}可用中文就診的醫院與診所 |  |
| cityTitle | English-speaking hospitals and clinics in {place} ({n}) | {place}可用中文就診的醫院與診所（{n}家） |  |
| cityDesc | {n} hospitals, clinics and dental clinics in {place} that list English support, with hours, appointment rules and phone numbers. | {place}登記可用中文（含台語、粵語）的醫院、診所與牙醫診所共{n}家，附看診時間、是否需預約及電話。 | 検索結果の説明文 |
| deptH1 | English-speaking {dept} in {place} | {place}可用中文就診的{dept} |  |
| deptTitle | English-speaking {dept} in {place} ({n}) | {place}可用中文就診的{dept}（{n}家） |  |
| clinicTitle | {name} – English support, hours and phone | {name}－中文對應、看診時間與電話 |  |

## zh-hans

| key | 英語（原文） | 訳案 | 意図 |
|---|---|---|---|
| tagline | Hospitals and clinics in Japan that accept patients in your language | 在日本可用中文就诊的医院和诊所 |  |
| tierA | Staff or interpreter | 工作人员或翻译 | ◎ 職員・通訳者が対応 |
| tierAdesc | The facility reports it can see patients in this language. | 该医疗机构申报可用此语言就诊。 |  |
| tierB | Phone or video interpreter | 电话或视频翻译 | ○ 電話・ビデオ通訳 |
| tierBdesc | Support is through a remote interpreting service. | 通过远程翻译服务提供协助。 |  |
| tierC | Translation device | 翻译设备 | △ 翻訳機、または要相談 |
| tierCdesc | Support relies on a translation device, or the facility asks you to consult first. | 借助翻译设备提供协助，或要求就诊前先咨询。 |  |
| tierD | Ask before visiting | 就诊前请先咨询 | ― 要相談で翻訳機なし（受診前に問い合わせを） |
| tierDdesc | The language is listed, but the facility asks you to consult first and has no translation device. | 已登记此语言，但需就诊前先咨询，且没有翻译设备。 |  |
| hospital | Hospital | 医院 |  |
| clinic | Clinic | 诊所 |  |
| dental | Dental clinic | 牙科诊所 |  |
| hol | Hol | 节假日 | 表の見出し（短く） |
| openNow | Open now | 正在接诊 |  |
| closedNow | Closed now | 非接诊时间 |  |
| bookingRequired | Appointment required | 需要预约 | ko/zh-hant は辞書（出典つき）の表現 |
| bookingNotRequired | Walk-ins accepted | 无需预约即可就诊 | ko/zh-hant は辞書（出典つき）の表現 |
| phone | Phone | 电话 |  |
| phoneForeign | Phone for foreign patients | 外国患者专用电话 |  |
| address | Address | 地址 |  |
| showDriver | Show this to a taxi driver | 请出示给出租车司机 |  |
| departments | Departments and hours | 科室与接诊时间 |  |
| otherDepts | Other departments (Japanese names) | 其他科室（日文名称） |  |
| payments | Cards and e-money | 信用卡与电子支付 |  |
| cashOnly | No cards or e-money reported | 未登记可用的信用卡或电子支付 |  |
| translationDevice | Translation device available | 备有翻译设备 |  |
| languages | Languages | 对应语言 |  |
| sources | Sources | 信息来源 |  |
| lastUpdated | Last updated by the facility | 医疗机构最后更新日 |  |
| disclaimer | Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit. | 信息由各医疗机构向厚生劳动省申报。接诊时间和语言支持可能变动，就诊前请先打电话确认。 |  |
| emergency | Emergency: call 119 (ambulance, free of charge) | 紧急情况请拨打119（救护车，免费） | 119番＝救急車（無料） |
| byDept | By department | 按科室 |  |
| allFacilities | All facilities | 全部医疗机构 |  |
| website | Website | 网站 |  |
| holidays | Hol = national holidays | 节假日＝日本法定节假日 |  |
| home | Home | 首页 |  |
| searchByArea | Search by area | 按地区查找 |  |
| howToRead | How to read the language support levels | 语言支持等级说明 |  |
| listedFirst | Facilities with staff or interpreters are listed first. | 有工作人员或翻译的医疗机构排在前面。 |  |
| srcMhlwNet | Medical Information Net (Ministry of Health, Labour and Welfare) | 医疗信息网（医療情報ネット・厚生劳动省） | 公式名「医療情報ネット」を併記 |
| srcD5 | List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare) | 外国患者接收医疗机构名单（厚生劳动省） |  |
| count | {n} facilities | {n}家 | 施設数の表示 |
| cityH1 | English-speaking hospitals and clinics in {place} | {place}可用中文就诊的医院和诊所 |  |
| cityTitle | English-speaking hospitals and clinics in {place} ({n}) | {place}可用中文就诊的医院和诊所（{n}家） |  |
| cityDesc | {n} hospitals, clinics and dental clinics in {place} that list English support, with hours, appointment rules and phone numbers. | {place}登记可用中文的医院、诊所和牙科诊所共{n}家，附接诊时间、是否需要预约和电话。 | 検索結果の説明文 |
| deptH1 | English-speaking {dept} in {place} | {place}可用中文就诊的{dept} |  |
| deptTitle | English-speaking {dept} in {place} ({n}) | {place}可用中文就诊的{dept}（{n}家） |  |
| clinicTitle | {name} – English support, hours and phone | {name}－中文支持、接诊时间和电话 |  |

## vi

| key | 英語（原文） | 訳案 | 意図 |
|---|---|---|---|
| tagline | Hospitals and clinics in Japan that accept patients in your language | Bệnh viện và phòng khám tại Nhật Bản có thể khám bằng tiếng Việt |  |
| tierA | Staff or interpreter | Nhân viên hoặc phiên dịch viên | ◎ 職員・通訳者が対応 |
| tierAdesc | The facility reports it can see patients in this language. | Cơ sở y tế cho biết có thể khám cho bệnh nhân bằng ngôn ngữ này. |  |
| tierB | Phone or video interpreter | Phiên dịch qua điện thoại hoặc video | ○ 電話・ビデオ通訳 |
| tierBdesc | Support is through a remote interpreting service. | Hỗ trợ thông qua dịch vụ phiên dịch từ xa. |  |
| tierC | Translation device | Máy phiên dịch | △ 翻訳機、または要相談 |
| tierCdesc | Support relies on a translation device, or the facility asks you to consult first. | Hỗ trợ bằng máy phiên dịch, hoặc cơ sở yêu cầu liên hệ trao đổi trước. |  |
| tierD | Ask before visiting | Hỏi trước khi đến | ― 要相談で翻訳機なし（受診前に問い合わせを） |
| tierDdesc | The language is listed, but the facility asks you to consult first and has no translation device. | Ngôn ngữ này có được đăng ký, nhưng cơ sở yêu cầu liên hệ trao đổi trước và không có máy phiên dịch. |  |
| hospital | Hospital | Bệnh viện |  |
| clinic | Clinic | Phòng khám |  |
| dental | Dental clinic | Phòng khám nha khoa |  |
| hol | Hol | Lễ | 表の見出し（短く） |
| openNow | Open now | Đang trong giờ khám |  |
| closedNow | Closed now | Ngoài giờ khám |  |
| bookingRequired | Appointment required | Cần đặt lịch hẹn | ko/zh-hant は辞書（出典つき）の表現 |
| bookingNotRequired | Walk-ins accepted | Khám không cần hẹn trước | ko/zh-hant は辞書（出典つき）の表現 |
| phone | Phone | Điện thoại |  |
| phoneForeign | Phone for foreign patients | Điện thoại dành cho bệnh nhân nước ngoài |  |
| address | Address | Địa chỉ |  |
| showDriver | Show this to a taxi driver | Đưa cho tài xế taxi xem |  |
| departments | Departments and hours | Khoa khám và giờ khám |  |
| otherDepts | Other departments (Japanese names) | Các khoa khác (tên tiếng Nhật) |  |
| payments | Cards and e-money | Thẻ và tiền điện tử |  |
| cashOnly | No cards or e-money reported | Không có thông tin về thẻ hoặc tiền điện tử |  |
| translationDevice | Translation device available | Có máy phiên dịch |  |
| languages | Languages | Ngôn ngữ hỗ trợ |  |
| sources | Sources | Nguồn |  |
| lastUpdated | Last updated by the facility | Ngày cơ sở cập nhật gần nhất |  |
| disclaimer | Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit. | Thông tin do từng cơ sở y tế báo cáo cho Bộ Y tế, Lao động và Phúc lợi Nhật Bản. Giờ khám và hỗ trợ ngôn ngữ có thể thay đổi. Vui lòng gọi điện trước khi đến. |  |
| emergency | Emergency: call 119 (ambulance, free of charge) | Cấp cứu: gọi 119 (xe cứu thương, miễn phí) | 119番＝救急車（無料） |
| byDept | By department | Theo khoa |  |
| allFacilities | All facilities | Tất cả cơ sở |  |
| website | Website | Trang web |  |
| holidays | Hol = national holidays | Lễ = ngày lễ quốc gia của Nhật Bản |  |
| home | Home | Trang chủ |  |
| searchByArea | Search by area | Tìm theo khu vực |  |
| howToRead | How to read the language support levels | Cách đọc mức hỗ trợ ngôn ngữ |  |
| listedFirst | Facilities with staff or interpreters are listed first. | Cơ sở có nhân viên hoặc phiên dịch viên được liệt kê trước. |  |
| srcMhlwNet | Medical Information Net (Ministry of Health, Labour and Welfare) | Mạng Thông tin Y tế (医療情報ネット, Bộ Y tế, Lao động và Phúc lợi) | 公式名「医療情報ネット」を併記 |
| srcD5 | List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare) | Danh sách cơ sở y tế tiếp nhận bệnh nhân nước ngoài (Bộ Y tế, Lao động và Phúc lợi) |  |
| count | {n} facilities | {n} cơ sở | 施設数の表示 |
| cityH1 | English-speaking hospitals and clinics in {place} | Bệnh viện và phòng khám nói tiếng Việt tại {place} |  |
| cityTitle | English-speaking hospitals and clinics in {place} ({n}) | Bệnh viện và phòng khám nói tiếng Việt tại {place} ({n}) |  |
| cityDesc | {n} hospitals, clinics and dental clinics in {place} that list English support, with hours, appointment rules and phone numbers. | {n} bệnh viện, phòng khám và phòng khám nha khoa tại {place} có đăng ký hỗ trợ tiếng Việt, kèm giờ khám, quy định đặt hẹn và số điện thoại. | 検索結果の説明文 |
| deptH1 | English-speaking {dept} in {place} | {dept} nói tiếng Việt tại {place} |  |
| deptTitle | English-speaking {dept} in {place} ({n}) | {dept} nói tiếng Việt tại {place} ({n}) |  |
| clinicTitle | {name} – English support, hours and phone | {name} – hỗ trợ tiếng Việt, giờ khám và điện thoại |  |

## pt

| key | 英語（原文） | 訳案 | 意図 |
|---|---|---|---|
| tagline | Hospitals and clinics in Japan that accept patients in your language | Hospitais e clínicas no Japão que atendem em português |  |
| tierA | Staff or interpreter | Funcionário ou intérprete | ◎ 職員・通訳者が対応 |
| tierAdesc | The facility reports it can see patients in this language. | A instituição informa que pode atender pacientes neste idioma. |  |
| tierB | Phone or video interpreter | Intérprete por telefone ou vídeo | ○ 電話・ビデオ通訳 |
| tierBdesc | Support is through a remote interpreting service. | O atendimento é feito por um serviço de interpretação remota. |  |
| tierC | Translation device | Aparelho de tradução | △ 翻訳機、または要相談 |
| tierCdesc | Support relies on a translation device, or the facility asks you to consult first. | O atendimento depende de um aparelho de tradução, ou a instituição pede consulta prévia. |  |
| tierD | Ask before visiting | Consulte antes de ir | ― 要相談で翻訳機なし（受診前に問い合わせを） |
| tierDdesc | The language is listed, but the facility asks you to consult first and has no translation device. | O idioma está registrado, mas a instituição pede consulta prévia e não tem aparelho de tradução. |  |
| hospital | Hospital | Hospital |  |
| clinic | Clinic | Clínica |  |
| dental | Dental clinic | Clínica odontológica |  |
| hol | Hol | Fer. | 表の見出し（短く） |
| openNow | Open now | Aberto agora |  |
| closedNow | Closed now | Fechado agora |  |
| bookingRequired | Appointment required | É necessário agendar | ko/zh-hant は辞書（出典つき）の表現 |
| bookingNotRequired | Walk-ins accepted | Atende sem agendamento | ko/zh-hant は辞書（出典つき）の表現 |
| phone | Phone | Telefone |  |
| phoneForeign | Phone for foreign patients | Telefone para pacientes estrangeiros |  |
| address | Address | Endereço |  |
| showDriver | Show this to a taxi driver | Mostre ao motorista de táxi |  |
| departments | Departments and hours | Especialidades e horários |  |
| otherDepts | Other departments (Japanese names) | Outras especialidades (nomes em japonês) |  |
| payments | Cards and e-money | Cartões e dinheiro eletrônico |  |
| cashOnly | No cards or e-money reported | Nenhum cartão ou dinheiro eletrônico informado |  |
| translationDevice | Translation device available | Possui aparelho de tradução |  |
| languages | Languages | Idiomas |  |
| sources | Sources | Fontes |  |
| lastUpdated | Last updated by the facility | Última atualização pela instituição |  |
| disclaimer | Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit. | As informações são fornecidas por cada instituição ao Ministério da Saúde, Trabalho e Bem-Estar do Japão. Horários e atendimento em idiomas podem mudar. Ligue antes de ir. |  |
| emergency | Emergency: call 119 (ambulance, free of charge) | Emergência: ligue 119 (ambulância, gratuita) | 119番＝救急車（無料） |
| byDept | By department | Por especialidade |  |
| allFacilities | All facilities | Todas as instituições |  |
| website | Website | Site |  |
| holidays | Hol = national holidays | Fer. = feriados nacionais do Japão |  |
| home | Home | Início |  |
| searchByArea | Search by area | Buscar por região |  |
| howToRead | How to read the language support levels | Como ler os níveis de atendimento em idiomas |  |
| listedFirst | Facilities with staff or interpreters are listed first. | Instituições com funcionários ou intérpretes aparecem primeiro. |  |
| srcMhlwNet | Medical Information Net (Ministry of Health, Labour and Welfare) | Rede de Informações Médicas (医療情報ネット, Ministério da Saúde, Trabalho e Bem-Estar) | 公式名「医療情報ネット」を併記 |
| srcD5 | List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare) | Lista de instituições médicas que aceitam pacientes estrangeiros (Ministério da Saúde, Trabalho e Bem-Estar) |  |
| count | {n} facilities | {n} instituições | 施設数の表示 |
| cityH1 | English-speaking hospitals and clinics in {place} | Hospitais e clínicas que atendem em português em {place} |  |
| cityTitle | English-speaking hospitals and clinics in {place} ({n}) | Hospitais e clínicas que atendem em português em {place} ({n}) |  |
| cityDesc | {n} hospitals, clinics and dental clinics in {place} that list English support, with hours, appointment rules and phone numbers. | {n} hospitais, clínicas e clínicas odontológicas em {place} com atendimento em português registrado, com horários, regras de agendamento e telefones. | 検索結果の説明文 |
| deptH1 | English-speaking {dept} in {place} | {dept} com atendimento em português em {place} |  |
| deptTitle | English-speaking {dept} in {place} ({n}) | {dept} com atendimento em português em {place} ({n}) |  |
| clinicTitle | {name} – English support, hours and phone | {name} – atendimento em português, horários e telefone |  |
