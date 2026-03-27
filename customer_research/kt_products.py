"""
KT B2B 상품 카탈로그
출처: KT Enterprise 소개자료 페이지 (https://enterprise.kt.com/cs/P_CS_BR_001.do)
카테고리 구조: AI / Cloud / 커뮤니케이션 서비스 / 데이터 서비스 / 모바일·IoT / Solutions
"""

KT_B2B_PRODUCTS: list[dict] = [

    # ══════════════════════════════════════════════
    # AI
    # ══════════════════════════════════════════════
    {
        "id": "sota_k",
        "name": "SOTA K (생성형 AI)",
        "category": "AI",
        "sub_category": "생성형 AI",
        "url": "https://enterprise.kt.com",
        "description": "KT 자체 개발 초거대 언어모델(LLM) 기반 생성형 AI 서비스. 기업 맞춤형 AI 어시스턴트·문서 자동화·업무 생산성 향상에 활용.",
        "use_cases": ["문서 자동 생성·요약", "업무 자동화", "기업 내부 챗봇", "콘텐츠 생성"],
        "keywords": ["생성형 AI", "LLM", "GenAI", "ChatGPT 대안", "AI 어시스턴트", "업무 자동화", "문서 요약"],
    },
    {
        "id": "k_intelligence_studio",
        "name": "K intelligence Studio Cloud (AI Studio)",
        "category": "AI",
        "sub_category": "AI Studio",
        "url": "https://enterprise.kt.com",
        "description": "기업이 자체 AI 모델을 개발·학습·배포할 수 있는 클라우드 AI 개발 플랫폼. 데이터 전처리부터 모델 서빙까지 통합 MLOps 환경 제공.",
        "use_cases": ["사내 AI 모델 개발", "MLOps 파이프라인 구축", "AI 서비스 내재화"],
        "keywords": ["AI 플랫폼", "MLOps", "머신러닝", "AI 개발", "모델 학습", "AI 내재화"],
    },
    {
        "id": "k_gpuaas",
        "name": "K GPUaaS (AI Infra)",
        "category": "AI",
        "sub_category": "AI Infra",
        "url": "https://enterprise.kt.com",
        "description": "AI 학습·추론에 특화된 GPU 클라우드 인프라 서비스. 대규모 AI 모델 학습 및 HPC 워크로드를 온디맨드로 사용.",
        "use_cases": ["대규모 AI 모델 학습", "GPU 인프라 구축", "HPC 워크로드 처리"],
        "keywords": ["GPU", "AI 인프라", "HPC", "딥러닝", "AI 학습", "클라우드 GPU"],
    },

    # ══════════════════════════════════════════════
    # Cloud
    # ══════════════════════════════════════════════
    {
        "id": "cloudflex",
        "name": "KT cloudflex",
        "category": "Cloud",
        "sub_category": "cloudflex",
        "url": "https://enterprise.kt.com",
        "description": "KT의 퍼블릭 클라우드 서비스. 서버·스토리지·DB·네트워크 등 풀스택 IaaS/PaaS 제공. 전국 IDC 기반 99.95% SLA 보장.",
        "use_cases": ["IT 인프라 현대화", "온프레미스 → 클라우드 전환", "DevOps·CI/CD 환경", "AI·빅데이터 플랫폼"],
        "keywords": ["클라우드", "IaaS", "PaaS", "DX", "인프라", "서버", "가상화", "하이브리드 클라우드"],
    },
    {
        "id": "managed_private_cloud",
        "name": "KT managed private cloud",
        "category": "Cloud",
        "sub_category": "managed private cloud",
        "url": "https://enterprise.kt.com",
        "description": "전용 하드웨어 기반 프라이빗 클라우드를 KT가 구축·운영 대행. 보안·컴플라이언스가 중요한 금융·공공·의료 기관에 최적.",
        "use_cases": ["금융·공공 규제 대응 클라우드", "데이터 주권 확보", "레거시 시스템 클라우드 전환"],
        "keywords": ["프라이빗 클라우드", "전용 클라우드", "금융 클라우드", "공공 클라우드", "규제 컴플라이언스"],
    },

    # ══════════════════════════════════════════════
    # 커뮤니케이션 서비스 — 스마트메시지
    # ══════════════════════════════════════════════
    {
        "id": "smart_message",
        "name": "KT 스마트메시지 (RCS·양방향문자·위치문자)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "스마트메시지",
        "url": "https://enterprise.kt.com",
        "description": "RCS·양방향 문자·위치문자·전자고지 등 기업 대량 문자 발송 서비스. 이미지·버튼·위치 정보를 포함한 고품질 메시지 전송.",
        "use_cases": ["마케팅 문자 발송", "전자고지서 발송", "고객 위치 안내", "예약·알림 자동화"],
        "keywords": ["문자", "RCS", "SMS", "MMS", "전자고지", "알림", "마케팅 문자", "대량 발송"],
    },
    {
        "id": "communis",
        "name": "KT Communis (카카오비즈메시지·알림톡)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "스마트메시지",
        "url": "https://enterprise.kt.com",
        "description": "카카오 알림톡·친구톡 등 카카오비즈메시지를 API로 연동·발송하는 기업 메시징 플랫폼.",
        "use_cases": ["카카오 알림톡 발송", "주문·배송 알림 자동화", "이벤트·쿠폰 발송"],
        "keywords": ["카카오", "알림톡", "친구톡", "메시지", "카카오비즈메시지", "알림"],
    },

    # ══════════════════════════════════════════════
    # 커뮤니케이션 서비스 — 전화
    # ══════════════════════════════════════════════
    {
        "id": "biz_pbx",
        "name": "KT 기업구내전화 (PBX)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "기업일반전화",
        "url": "https://enterprise.kt.com",
        "description": "사무실 내 구내교환기(PBX) 솔루션. 내선 통화·당겨받기·착신전환 등 기업 전화 환경 구성.",
        "use_cases": ["사무실 내선 전화 구축", "PBX 신규 도입"],
        "keywords": ["PBX", "구내전화", "내선", "사무실 전화", "교환기"],
    },
    {
        "id": "biz_voip",
        "name": "KT 기업인터넷전화 (Centrex·biz)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "기업인터넷전화",
        "url": "https://enterprise.kt.com",
        "description": "인터넷 기반 기업 전화 서비스. Centrex형(KT 국사 수용)과 biz형 제공. Microsoft Teams Phone 연동 지원.",
        "use_cases": ["PBX 노후화 대체", "클라우드 전화 전환", "재택·하이브리드 근무 통신", "Teams 전화 연동"],
        "keywords": ["인터넷전화", "VoIP", "Centrex", "Teams Phone", "UC", "재택근무", "클라우드 전화"],
    },
    {
        "id": "lingo_biz",
        "name": "KT 링고비즈 (전화부가서비스)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "전화부가서비스",
        "url": "https://enterprise.kt.com",
        "description": "발신번호 표시·플러스링·멘트 설정 등 기업 전화 부가서비스. 브랜드 전화번호로 신뢰감 있는 고객 응대.",
        "use_cases": ["발신번호 브랜딩", "고객 응대 품질 향상"],
        "keywords": ["발신번호", "링고", "전화 부가서비스", "브랜드 전화"],
    },
    {
        "id": "representative_number",
        "name": "KT 전국대표번호·수신자부담 (지능망)",
        "category": "커뮤니케이션 서비스",
        "sub_category": "지능망",
        "url": "https://enterprise.kt.com",
        "description": "전국대표번호(1588·1600 등)·수신자부담 080·안심번호 0502 등 기업용 지능망 서비스.",
        "use_cases": ["전국 단일 대표번호 운영", "고객 무료 수신 제공", "번호 노출 없는 안심 상담"],
        "keywords": ["대표번호", "1588", "080", "수신자부담", "안심번호", "고객센터 번호"],
    },

    # ══════════════════════════════════════════════
    # 데이터 서비스
    # ══════════════════════════════════════════════
    {
        "id": "cloudline",
        "name": "KT cloudline",
        "category": "데이터 서비스",
        "sub_category": "cloudline",
        "url": "https://enterprise.kt.com",
        "description": "클라우드 직접 연결 전용 회선. KT Cloud·AWS·Azure 등 주요 클라우드로 안정적인 프라이빗 연결 제공.",
        "use_cases": ["클라우드 직접 연결", "하이브리드 클라우드 구성", "데이터 전송 안정성 확보"],
        "keywords": ["클라우드 전용선", "Direct Connect", "클라우드 연결", "하이브리드"],
    },
    {
        "id": "giga_office",
        "name": "KT GiGA Office",
        "category": "데이터 서비스",
        "sub_category": "기업인터넷",
        "url": "https://enterprise.kt.com",
        "description": "기업 전용 인터넷 회선 + 구내 WiFi를 결합한 통합 서비스. 소호·중소기업 대상으로 인터넷·전화·WiFi를 하나의 계약으로 제공.",
        "use_cases": ["소호·중소기업 인터넷 구축", "사무실 WiFi 통합", "인터넷+전화 결합"],
        "keywords": ["기업인터넷", "WiFi", "소호", "중소기업", "GiGA Office", "유선인터넷"],
    },
    {
        "id": "kornet",
        "name": "KT Kornet",
        "category": "데이터 서비스",
        "sub_category": "기업인터넷",
        "url": "https://enterprise.kt.com",
        "description": "기업 전용 고속 인터넷 회선 서비스. 안정적인 대역폭·SLA·고정 IP를 제공하며 대기업·공공기관에 적합.",
        "use_cases": ["대기업·공공기관 인터넷 회선", "고정IP·SLA 보장 인터넷", "본사-지점 간 안정적 연결"],
        "keywords": ["Kornet", "기업인터넷", "전용인터넷", "고정IP", "SLA", "대기업"],
    },
    {
        "id": "flexline",
        "name": "KT Flexline (기업인터넷)",
        "category": "데이터 서비스",
        "sub_category": "기업인터넷",
        "url": "https://enterprise.kt.com",
        "description": "SD-WAN 기반 기업 전용 인터넷. 유연한 대역폭 조정·회선·IP·장비·모니터링 통합 제공. GiGA Office, Kornet, VPN 등 라인업 포함.",
        "use_cases": ["기업 인터넷 현대화", "다지점 네트워크 통합", "클라우드 연결 최적화"],
        "keywords": ["기업인터넷", "SD-WAN", "Flexline", "GiGA Office", "VPN", "네트워크"],
    },
    {
        "id": "dedicated_line",
        "name": "KT 전용회선 (국내·방송·양자암호)",
        "category": "데이터 서비스",
        "sub_category": "전용회선",
        "url": "https://enterprise.kt.com",
        "description": "국내 전용회선·방송 전용회선·양자암호 전용회선 제공. 고보안이 필요한 금융·방송·공공 전용망 구성.",
        "use_cases": ["거점 간 전용망 구성", "방송 중계망", "양자암호 보안 통신", "금융 전용망"],
        "keywords": ["전용회선", "양자암호", "방송회선", "전용망", "보안회선", "금융망"],
    },
    {
        "id": "managed",
        "name": "KT 매니지드 (네트워크 운영 대행)",
        "category": "데이터 서비스",
        "sub_category": "매니지드",
        "url": "https://enterprise.kt.com",
        "description": "기업 네트워크 장비·회선 운영을 KT가 대행. 매니지드ON(통합 포털)으로 실시간 현황 모니터링.",
        "use_cases": ["네트워크 운영 인력 절감", "24시간 장애 대응", "통합 네트워크 관제"],
        "keywords": ["매니지드", "네트워크 관리", "운영 대행", "아웃소싱", "모니터링"],
    },
    {
        "id": "biz_success_pack",
        "name": "KT 비즈성공팩 (결합패키지)",
        "category": "데이터 서비스",
        "sub_category": "결합패키지",
        "url": "https://enterprise.kt.com",
        "description": "인터넷·전화·모바일 등 KT B2B 서비스를 묶은 결합 패키지. 소상공인·중소기업 대상 비용 절감형 통합 상품.",
        "use_cases": ["중소기업 통신비 절감", "인터넷+전화 통합 계약"],
        "keywords": ["결합상품", "패키지", "중소기업", "소상공인", "통신비 절감"],
    },

    # ══════════════════════════════════════════════
    # 모바일/IoT
    # ══════════════════════════════════════════════
    {
        "id": "biz_5g",
        "name": "KT 5G 업무망 (기업전용5G)",
        "category": "모바일/IoT",
        "sub_category": "기업전용5G",
        "url": "https://enterprise.kt.com",
        "description": "기업 임직원 전용 5G 업무망. 일반 상용망과 분리된 전용 네트워크로 보안·품질 보장. 로밍 서비스 포함.",
        "use_cases": ["임직원 전용 5G 업무망", "보안 모바일 업무 환경", "해외 출장 로밍"],
        "keywords": ["5G", "기업전용5G", "업무망", "모바일 보안", "로밍", "임직원"],
    },
    {
        "id": "office_mobile",
        "name": "KT 오피스모바일 (기업모바일)",
        "category": "모바일/IoT",
        "sub_category": "기업모바일",
        "url": "https://enterprise.kt.com",
        "description": "법인 명의 모바일 서비스. 임직원 전용 요금제·기기 할부·통합 청구 관리.",
        "use_cases": ["임직원 법인폰 관리", "통신비 통합 청구", "단말 할부 일괄 관리"],
        "keywords": ["법인폰", "모바일", "임직원", "오피스모바일", "통신비", "기업 요금제"],
    },
    {
        "id": "sky_auto",
        "name": "KT skyAuto (기업특화서비스)",
        "category": "모바일/IoT",
        "sub_category": "기업특화 서비스",
        "url": "https://enterprise.kt.com",
        "description": "기업 차량 관제·운행 관리 서비스. GPS 기반 실시간 위치 추적·운행 기록·안전 운전 관리.",
        "use_cases": ["법인 차량 관제", "운행 기록 관리", "배달·물류 차량 추적"],
        "keywords": ["차량관제", "GPS", "법인차량", "운행관리", "물류", "배달"],
    },
    {
        "id": "iot",
        "name": "KT IoT (LPWA·LTE·5G IoT)",
        "category": "모바일/IoT",
        "sub_category": "IoT",
        "url": "https://enterprise.kt.com",
        "description": "LPWA·LTE·5G 기반 기업 IoT 회선 및 단말 연결 서비스. 원격 검침·자산 추적·환경 모니터링 등 다양한 IoT 서비스 지원.",
        "use_cases": ["원격 검침", "자산·재고 추적", "냉장·물류 모니터링", "환경 센서 연결"],
        "keywords": ["IoT", "LPWA", "LTE IoT", "5G IoT", "원격검침", "자산추적", "스마트센서"],
    },

    # ══════════════════════════════════════════════
    # Solutions — AICC/콜센터
    # ══════════════════════════════════════════════
    {
        "id": "acen_cloud",
        "name": "KT A'Cen Cloud (AICC)",
        "category": "Solutions",
        "sub_category": "AICC/콜센터",
        "url": "https://enterprise.kt.com",
        "description": "클라우드 기반 AI 컨택센터. AI 음성봇·챗봇·상담 어시스턴트 통합. 하루 10만 건 이상 상담 자동 처리 가능.",
        "use_cases": ["콜센터 AI 전환", "24시간 자동 고객 응대", "상담 품질 분석", "ARS 고도화"],
        "keywords": ["AICC", "AI 콜센터", "음성봇", "챗봇", "상담 자동화", "A'Cen", "고객센터"],
    },
    {
        "id": "acen_onpremise",
        "name": "KT A'Cen On-Premise (AICC)",
        "category": "Solutions",
        "sub_category": "AICC/콜센터",
        "url": "https://enterprise.kt.com",
        "description": "구축형 AI 컨택센터. 보안·컴플라이언스가 중요한 기업의 사내 서버 환경에 AI 콜센터 직접 구축.",
        "use_cases": ["금융·공공 AI 콜센터 내재화", "보안 요건이 높은 콜센터 구축"],
        "keywords": ["AICC", "온프레미스", "구축형 AI 콜센터", "내재화", "금융 콜센터"],
    },
    {
        "id": "callcenter_custom",
        "name": "KT 콜센터 커스텀 (Pro)",
        "category": "Solutions",
        "sub_category": "AICC/콜센터",
        "url": "https://enterprise.kt.com",
        "description": "기업 맞춤형 클라우드 콜센터 솔루션. 콜센터 커스텀·커스텀 Pro 두 가지 플랜으로 소규모부터 대형 콜센터까지 지원.",
        "use_cases": ["신규 콜센터 구축", "기존 콜센터 클라우드 전환", "콜센터 운영 비용 절감"],
        "keywords": ["콜센터", "클라우드 콜센터", "상담", "고객센터 구축"],
    },

    # ══════════════════════════════════════════════
    # Solutions — Security
    # ══════════════════════════════════════════════
    {
        "id": "secure_utm",
        "name": "KT Secure UTM (보안)",
        "category": "Solutions",
        "sub_category": "Security",
        "url": "https://enterprise.kt.com",
        "description": "방화벽·IPS·VPN·바이러스 차단을 통합한 UTM(통합위협관리) 보안 장비 서비스. 중소기업도 쉽게 엔터프라이즈급 보안 구현.",
        "use_cases": ["중소기업 네트워크 보안", "방화벽 구축", "악성코드·바이러스 차단"],
        "keywords": ["UTM", "방화벽", "보안", "IPS", "바이러스 차단", "네트워크 보안"],
    },
    {
        "id": "ai_mail_security",
        "name": "KT AI 메일보안",
        "category": "Solutions",
        "sub_category": "Security",
        "url": "https://enterprise.kt.com",
        "description": "AI 기반 이메일 보안 서비스. 피싱·스팸·악성 첨부파일을 AI가 실시간 탐지·차단.",
        "use_cases": ["피싱 메일 차단", "랜섬웨어 예방", "이메일 보안 강화"],
        "keywords": ["이메일 보안", "피싱", "스팸", "랜섬웨어", "AI 보안", "메일보안"],
    },
    {
        "id": "cleanzone",
        "name": "KT 클린존 (보안)",
        "category": "Solutions",
        "sub_category": "Security",
        "url": "https://enterprise.kt.com",
        "description": "인터넷 구간 악성코드·유해 사이트 차단 서비스. 별도 장비 없이 네트워크 레벨에서 보안 위협 필터링.",
        "use_cases": ["유해 사이트 차단", "악성코드 감염 예방", "임직원 인터넷 보안"],
        "keywords": ["클린존", "유해차단", "악성코드", "보안 필터링", "인터넷 보안"],
    },

    # ══════════════════════════════════════════════
    # Solutions — CCTV AI 영상분석
    # ══════════════════════════════════════════════
    {
        "id": "cctv_ai",
        "name": "KT CCTV AI 영상분석",
        "category": "Solutions",
        "sub_category": "CCTV AI 영상분석",
        "url": "https://enterprise.kt.com",
        "description": "기존 CCTV에 AI를 결합해 이상행동·침입·화재·안전모 미착용 등을 실시간 감지·알림.",
        "use_cases": ["공장 안전 관리", "건설 현장 안전모 감지", "무인 매장 이상 감지", "침입 감지"],
        "keywords": ["CCTV", "AI 영상분석", "안전관리", "침입감지", "스마트 보안", "영상 AI"],
    },

    # ══════════════════════════════════════════════
    # Solutions — Works (업무 솔루션)
    # ══════════════════════════════════════════════
    {
        "id": "bizmecar_ez",
        "name": "비즈메카 EZ (Works)",
        "category": "Solutions",
        "sub_category": "Works",
        "url": "https://enterprise.kt.com",
        "description": "중소기업용 클라우드 그룹웨어. 전자결재·업무일지·게시판·메신저 등 기업 협업 기능 통합 제공.",
        "use_cases": ["전자결재 도입", "사내 협업 플랫폼 구축", "중소기업 그룹웨어"],
        "keywords": ["그룹웨어", "전자결재", "협업", "비즈메카", "중소기업 솔루션", "사내 메신저"],
    },

    # ══════════════════════════════════════════════
    # Solutions — 에너지
    # ══════════════════════════════════════════════
    {
        "id": "giga_energy_trade",
        "name": "KT GiGA energy trade (에너지)",
        "category": "Solutions",
        "sub_category": "에너지",
        "url": "https://enterprise.kt.com",
        "description": "기업 간 재생에너지 거래 플랫폼. RE100 이행을 위한 태양광·풍력 등 재생에너지 구매·판매 중개.",
        "use_cases": ["RE100 이행", "ESG 탄소중립 대응", "재생에너지 구매"],
        "keywords": ["RE100", "ESG", "탄소중립", "재생에너지", "에너지 거래", "GiGA energy"],
    },

    # ══════════════════════════════════════════════
    # Solutions — 공간 솔루션
    # ══════════════════════════════════════════════
    {
        "id": "safemate",
        "name": "KT SafeMate (방범·소방안전)",
        "category": "Solutions",
        "sub_category": "공간 솔루션",
        "url": "https://enterprise.kt.com",
        "description": "IoT 센서 기반 스마트 방범·소방 안전 솔루션. 침입 감지·화재 감지·비상 알림을 통합 관리.",
        "use_cases": ["사무실·점포 방범", "소방 안전 관리", "스마트빌딩 보안"],
        "keywords": ["방범", "소방안전", "SafeMate", "IoT 보안", "스마트빌딩", "화재감지"],
    },
    {
        "id": "air_map",
        "name": "KT Air Map (공간 솔루션)",
        "category": "Solutions",
        "sub_category": "공간 솔루션",
        "url": "https://enterprise.kt.com",
        "description": "실내 공기질(미세먼지·CO2·온습도 등) 실시간 모니터링·관리 솔루션. 학교·병원·사무실 등 다중이용시설 최적.",
        "use_cases": ["사무실·학교 공기질 관리", "ESG 환경 관리", "스마트빌딩 환경 제어"],
        "keywords": ["공기질", "미세먼지", "실내환경", "ESG", "스마트빌딩", "환경모니터링"],
    },

    # ══════════════════════════════════════════════
    # Solutions — 광고/마케팅
    # ══════════════════════════════════════════════
    {
        "id": "addressable_tv",
        "name": "KT Addressable TV Basic (광고/마케팅)",
        "category": "Solutions",
        "sub_category": "광고/마케팅",
        "url": "https://enterprise.kt.com",
        "description": "IPTV 기반 타깃 광고 플랫폼. 가구별 맞춤 광고 송출로 기존 TV 광고 대비 높은 광고 효율 제공.",
        "use_cases": ["타깃 TV 광고 집행", "지역 기반 광고", "가구 맞춤 광고"],
        "keywords": ["TV 광고", "어드레서블 TV", "IPTV 광고", "타깃 광고", "마케팅"],
    },
    {
        "id": "k_ads",
        "name": "K-Ads / 생활이동분석솔루션 PLIP (광고/마케팅)",
        "category": "Solutions",
        "sub_category": "광고/마케팅",
        "url": "https://enterprise.kt.com",
        "description": "KT 통신 빅데이터 기반 광고·분석 플랫폼. 유동인구·생활이동 분석으로 상권 분석·타깃 마케팅 지원.",
        "use_cases": ["상권 분석", "타깃 마케팅", "유동인구 분석", "출점 입지 분석"],
        "keywords": ["빅데이터", "유동인구", "상권분석", "타깃마케팅", "K-Ads", "PLIP"],
    },

    # ══════════════════════════════════════════════
    # Solutions — 미디어/교육
    # ══════════════════════════════════════════════
    {
        "id": "giniv_tv_biz",
        "name": "지니TV Biz (미디어/교육)",
        "category": "Solutions",
        "sub_category": "미디어/교육",
        "url": "https://enterprise.kt.com",
        "description": "기업·기관 전용 IPTV 서비스. 호텔·병원·사무실 등 로비·객실용 채널 편성 및 사내 방송 제공.",
        "use_cases": ["호텔 객실 TV", "병원 대기실 IPTV", "사내 방송", "교육 콘텐츠 방영"],
        "keywords": ["IPTV", "지니TV", "호텔TV", "병원TV", "사내방송", "교육방송"],
    },
    {
        "id": "ai_education",
        "name": "KT AI 미래교육 (미디어/교육)",
        "category": "Solutions",
        "sub_category": "미디어/교육",
        "url": "https://enterprise.kt.com",
        "description": "학교·교육기관 대상 AI 기반 미래교육 솔루션. AI 코딩·디지털 리터러시 교육 콘텐츠·플랫폼 제공.",
        "use_cases": ["학교 AI 교육 도입", "디지털 교육 전환", "코딩 교육"],
        "keywords": ["AI 교육", "미래교육", "에듀테크", "코딩", "디지털교육", "학교"],
    },
]


# 브로슈어 보유 상품 ID 목록 (RAG 인덱스에 포함된 11개)
BROCHURE_PRODUCT_IDS = {
    "sota_k", "k_intelligence_studio", "k_gpuaas",
    "cloudflex", "managed_private_cloud",
    "giga_office", "kornet", "flexline",
    "biz_5g", "secure_utm", "giga_energy_trade",
}

BROCHURE_PRODUCTS = [p for p in KT_B2B_PRODUCTS if p["id"] in BROCHURE_PRODUCT_IDS]


def get_all_products() -> list[dict]:
    return KT_B2B_PRODUCTS


def get_products_by_category(category: str) -> list[dict]:
    return [p for p in KT_B2B_PRODUCTS if p["category"] == category]


def get_products_by_sub_category(sub_category: str) -> list[dict]:
    return [p for p in KT_B2B_PRODUCTS if p.get("sub_category") == sub_category]


CATEGORIES = sorted({p["category"] for p in KT_B2B_PRODUCTS})
SUB_CATEGORIES = sorted({p["sub_category"] for p in KT_B2B_PRODUCTS})
