# CLI, Docker 및 Kubernetes(참조 레이아웃)

## CLI 자동화

이 장은 Microsoft/HashiCorp 스타일(사용 라인, 플래그 테이블(영어 토큰)), 복사-붙여넣기 예제를 따릅니다.

CLI(OrganizeFiles.Cli)
  사용법: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  사용법: OrganizeFiles.Cli --output <dir> --mode repair [options]

  깃발 (긴) | 의미
  -------------------------|---------------
  --execute | 실제 이동(기본값은 드라이런만임)
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | B64가 포함된 UTF-8 재개 상태 파일| 윤곽.
  --delete-duplicates | 중복 후보를 삭제합니다(--execute 와 함께 --confirm-delete 필요).
  --delete-issues | 이슈 버킷 후보를 삭제합니다(--execute 와 함께 --confirm-delete 필요). 원격 자동화 대상에는 없습니다.
  --archive-after-organize | 정리 후: 파일별 형제 ZIP을 사용한 다음 원본을 삭제합니다(--execute 와 함께 --confirm-delete 필요). 이미 아카이브된 확장을 건너뜁니다.

  **참고:** CLI `--mode models`는 AI 아티팩트가 아닌 **CAD/3D 모델**을 선택합니다. AI/ML에는 `--mode ai` 또는 `--mode models-ai`를 사용하세요.

  예(드라이런, 모든 버킷): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  예(고유 이동만 실행): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  빌드: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  드라이런: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  --execute 의 경우 소스 마운트에서 :ro를 제거합니다. 다중 worker 규칙(worker당 하나의 출력 루트)은 containers/README.md를 참조하세요.

Kubernetes(참조 작업)
  읽기 전용 소스 PVC는 테스트 실행 작업에 유효합니다. --execute 를 실제로 사용하려면 쓰기 가능한 소스 PVC가 필요합니다. 모든 정리/복구 실행(드라이런 및 실행)에 대해 유효한 저장소 또는 게시자 권한을 제공하세요. 출력 트리당 하나의 Pod입니다. 최소 패턴은 샘플 매니페스트와 함께 containers/README.md에 문서화되어 있습니다.

작업 진행 상황
  작업 창은 App, CLI, Docker 및 Kubernetes 실행의 진행 상황을 보여 줍니다. 총계를 아는 단계는 백분율을 표시합니다. 총계가 없는 검색은 미정 상태로 남습니다.
  자동화는 ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 으로 CLI worker를 시작하고 그 표시 줄을 보이는 기록에서 제거합니다. 손으로 시작한 CLI 실행은 그 변수가 설정되지 않는 한 표시를 내보내지 않습니다.
  Docker 와 Kubernetes worker도 같은 변수를 받으므로 그 실행도 백분율을 알립니다. 이 수치는 worker의 로그에서 읽어 오므로 컨테이너나 파드가 로그를 쓰기 시작할 때부터 나타납니다.
  --list-running 과 --show-run 은 실행이 무언가를 알린 경우 활성 작업의 진행 상황 필드를 담습니다.

# 예제 실행

## 그래픽 UI

**소스** 와 출력 폴더를 추가하고 실행 모드를 선택한 다음, 미리 보기를 위해 **드라이런** 을 켜고 **실행** 을 누릅니다. 실제로 이동하려면 **드라이런** 을 끔 상태로 둡니다. 삭제 옵션은 실행 전에 확인을 요청합니다.

## CLI 예제

CLI 드라이런: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
