import os, sys # 파이썬 인터프리터를 제어할 수 있는 방법을 제공, 운영체제(OS : Operating System)를 제어

if os.name == 'nt': # Windows를 실행 중임을 의미, 운영 체제("os")가 window임을 의미
    import msvcrt # window 운영체제에서 제공됨, 대부분이 콘솔의 입출력, 키보드 입력 및 화면 출력과 연관
    def getch():
        return msvcrt.getch().decode() # 키 누르기를 읽고 결과 문자를 바이트열로 반환, 바이트 문자열을 유니코드 문자열(문자열)로 디코딩
    
else:  
    import tty, termios # tty = 정보를 컴퓨터에 입력하고 정보를 가져옴 (현재 커널과 연결된 가상 터미널 장치 이름을 알 수 있다)

    # 단일 키 누르기를 감지하려면, linux의 경우 sys, tty, termios 를 import 하여야 한다.
    
    fd = sys.stdin.fileno() 

    # 유닉스 계열 시스템에서, 파일을 열 때, 시스템은 사용자가 작동하는 파일 기술자(정수)를 사용
    # 열린 파일을 나타내는 정수입니다. 열려 있는 각 파일에는 고유한 파일 디스크립터가 주어짐
    # 세 개의 표준 파일 디스크립터(표준 입력, 표준 출력 및 표준 오류)가 있으며 파일 디스크립터는 각각 0, 1, 2

    old_settings = termios.tcgetattr(fd) # 백업 및 복원 역할
    tty.setraw(sys.stdin.fileno()) 

    # 표준 입력 스트림(프로그램이 사용자로부터 입력을 받는 데 사용되는 데이터 스트림)을 
    # 원시 모드(일반적으로 텍스트나 다른 형식으로 처리되지 않은 데이터)로 변경하는 것 
    # 즉 특수 문자를 포함한 모든 문자가 전송 중에 이스케이프(특정 문자나 문자열을 다른 의미로 해석하지 않고 문자 그대로 사용하기 위해 사용되는 메커니즘)되지 않음. ex) \n, \t
    # 모드를 변경하기 전에 원래 모드를 백업하고 변경 후 복원

    def getch():
        return sys.stdin.read(1) # 한줄 단위로 입력받음

os.sys.path.append('../dynamixel_functions_py')             # 경로 설정 (추가)

import dynamixel_functions as dynamixel                     # DYNALEX SDK 라이브러리 사용

# 제어 테이블 주소
ADDR_PRO_TORQUE_ENABLE       = 562                          # 토크 활성화 주소
ADDR_PRO_GOAL_POSITION       = 596                          # 목표 위치 주소
ADDR_PRO_PRESENT_POSITION    = 611                          # 현재 위치 주소

# Protocol version
PROTOCOL_VERSION            = 2                             # Dynamixel에서 사용되는 프로토콜 버전 보기 (이 코드는 파이썬 프로토콜 2.0 버전임)

# 기본 설정
DXL1_ID                     = 1                             # Dynamixel ID: 1, ex) 왼쪽 바퀴
DXL2_ID                     = 2                             # Dynamixel ID: 2, ex) 오른쪽 바퀴
BAUDRATE                    = 1000000                       

# 전송 속도가 1,000,000 비트/초(bps), 시리얼 통신에서 사용되는 데이터 전송 속도를 나타내는 매개변수

DEVICENAME1                 = "/dev/ttyUSB0".encode('utf-8')

# 디바이스 파일 경로,  "/dev/ttyUSB0"은 컴퓨터의 USB 0번째 시리얼 포트와 같은 직렬 통신 장치를 나타냄, 
# .encode('utf-8')은 문자열을 UTF-8 인코딩으로 바이트열로 변환하는 역할
# "tty" = teletype, 리눅스 디바이스 드라이브(데이터를 저장하는 물리적인 장치 + 엑세스 역할) 장치중에 콘솔 (모니터, 키보드로 직접 본체에 연결된 모드) 혹은
# 터미널 (본체에 LAN으로 연결된 모드) 을 의미 (엑세스는 컴퓨터 시스템에서 데이터나 리소스에 대한 권한을 제어하는 것을 의미)

DEVICENAME2                 = "/dev/ttyUSB1".encode('utf-8')        # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"

TORQUE_ENABLE               = 1                             # 기본 설정 토크를 활성화하기 위한 값
TORQUE_DISABLE              = 0                             # 토크 (물체가 회전하는 데 필요한 힘 또는 에너지 or 회전력) 비활성화 값
DXL_MINIMUM_POSITION_VALUE  = -150000                       # 다이나믹셀 모터의 위치 제어에서 사용되는 최소 위치 값, 최소한 -150000의 위치까지 이동할 수 있음
DXL_MAXIMUM_POSITION_VALUE  = 150000                        # 이 값(위치 값이 이동 가능한 범위를 벗어나면 Dynamixel이 움직이지 않음)
DXL_MOVING_STATUS_THRESHOLD = 10                            # 움직임의 유무를 판별하는 기준 속도로 사용

ESC_ASCII_VALUE             = 0x1b

COMM_SUCCESS                = 0                             # 통신 결과 값
COMM_TX_FAIL                = -1001                         # 통신 Tx 실패

# 포트 핸들러 구조물 초기화
# 포트 경로 설정
# PortHandlerLinux 또는 PortHandlerWindows의 메서드 및 멤버 가져오기

port_num1 = dynamixel.portHandler(DEVICENAME1) 

# port_num1 = DEVICENAME1에 지정된 시리얼 포트와의 통신을 관리하기 위한 핸들러, 이 핸들러를 통해 모터와 데이터를 송수신하고 제어할 수 있음
# portHandler() 기능은 포트 경로를 and, get, 각각 설정하고, 컨트롤러 OS에서 포트 제어를 위한 적절한 기능을 자동으로 준비함

port_num2 = dynamixel.portHandler(DEVICENAME2)

# packetHandler() 구조 초기화

dynamixel.packetHandler()

# packHandler() 함수는 패킷 생성 및 패킷 저장에 사용되는 매개 변수를 초기화함
# 패킷 = 네트워크를 통해 전송되는 형식화된 데이터 덩어리

index = 0
dxl_comm_result = COMM_TX_FAIL                              # 다이나믹셀 모터와의 송신 통신이 실패했음을 나타냄을 dxl_comm_result 변수에 넣음
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Dynamixel 모터의 목표 위치를 나타내는 리스트 (다이나믹셀 회전의 목표 포인트를 저장)

dxl_error = 0                                               # Dynamixel error
dxl1_present_position = 0                                   # Present position
dxl2_present_position = 0

# Open port1 -> 컨트롤러가 다이나믹셀과 시리얼 통신하기 위해 포트를 열음
if dynamixel.openPort(port_num1): 
    print("Succeeded to open the port!")
else:
    print("Failed to open the port!")
    print("Press any key to terminate...")
    getch()
    quit()

# Open port2
if dynamixel.openPort(port_num2):
    print("Succeeded to open the port!")
else:
    print("Failed to open the port!")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port1 baudrate -> 통신 baudrate를 설정
if dynamixel.setBaudRate(port_num1, BAUDRATE): # port_num1 = 시리얼 포트 번호, BAUDRATE = 통신 속도를 설정
    print("Succeeded to change the baudrate!")
else:
    print("Failed to change the baudrate!")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port2 baudrate
if dynamixel.setBaudRate(port_num2, BAUDRATE):
    print("Succeeded to change the baudrate!")
else:
    print("Failed to change the baudrate!")
    print("Press any key to terminate...")
    getch()
    quit()


# Enable Dynamixel#1 Torque
dynamixel.write1ByteTxRx(port_num1, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE) # Dynamixel 모터에게 토크를 켜도록 지시

# 함수는 통신 프로토콜의 #과 # 다이나믹셀에 # 포트와 # 포트를 통해 명령어를 보내고, address에 1 byte의 값을 씁니다. 이 함수는 Tx/Rx 결과를 확인하고 하드웨어 오류를 수신함
# function 및 function get 중 하나를 얻은 다음 function 및 function 통신 오류 또는 하드웨어 오류가 발생한 경우 콘솔창에 결과를 표시함 
# Rx = 수신신호가 들어오는 곳, Tx = 송신신호선이 나가는 곳

# port_num1= Dynamixel 모터와 통신하는 포트
# DXL1_ID = 명령을 보낼 Dynamixel 모터의 고유 ID
# ADDR_PRO_TORQUE_ENABLE = 모터의 토크 활성화 주소를 나타냄
# TORQUE_ENABLE = 해당 토크를 활성화하기 위해 설정하려는 값

if dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION) != COMM_SUCCESS: # dynamixel.getLastTxRxResult()함수는 가장 최근에 수행된 통신의 결과를 반환
    dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION)) # 통신 실패시 통신 결과를 출력 (프로토콜 버전과 통신 결과가 전달)
elif dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION) != 0: # 가장 최근에 수신된 패킷의 오류 번호를 반환
    dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION)) # 최근 수신된 패킷의 오류가 0이 아니라면 (즉, 오류가 발생했다면), 해당 오류를 출력
else:
    print("Dynamixel#1 has been successfully connected")

# Enable Dynamixel #2 Torque
dynamixel.write1ByteTxRx(port_num2, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION) != COMM_SUCCESS:
    dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION))
elif dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION) != 0:
    dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION))
else:
    print("Dynamixel#2 has been successfully connected")


while 1: # 무한 루프
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(ESC_ASCII_VALUE): # getch()" 함수를 사용하여 사용자의 키 입력을 읽어옴,  사용자가 입력한 값이 ESC 키의 ASCII 값과 동일한지 확인
        break # ESC 눌렀다면 break문 실행

    # Write Dynamixel #1 goal position -> Dynamixel 모터에 목표 위치 값을 설정하고, 통신 결과 및 수신된 패킷 오류를 확인
    dynamixel.write4ByteTxRx(port_num1, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_GOAL_POSITION, dxl_goal_position[index])

    # 4바이트 데이터를 전송하여 모터의 위치를 설정
    # ADDR_PRO_GOAL_POSITION`: 서보 모터에서 목표 위치 값이 저장된 주소
 `  # dxl_goal_position[index]`: 설정하려는 목표 위치 값 

    if dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION) != COMM_SUCCESS: 
        # dynamixel.getLastTxRxResult()함수는 포트 번호와 프로토콜 버전을 인자로 받아 마지막으로 송수신된 결과를 반환
        # 목표 위치 값의 전송 및 수신이 성공했는지 확인

        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION)) 
        # 이전에 전송된 패킷의 전송 및 수신 결과를 확인하고, 그 결과를 출력하는 역할 (두 개의 인자를 받아 해당 정보를 출력)

    elif dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION) != 0: # 전송 및 수신이 성공한 경우 (0이면 오류), 수신된 패킷에 오류가 있는지 확인
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION))
        # 마지막으로 수신한 패킷의 오류 상태를 확인하고, 해당 오류 정보를 출력하는 역할
        
    # Write Dynamixel #2 goal position
    dynamixel.write4ByteTxRx(port_num2, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_GOAL_POSITION, dxl_goal_position[index])
    if dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION) != COMM_SUCCESS:
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION))
    elif dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION) != 0:
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION))

    while 1:
        # Read present position
        dxl1_present_position = dynamixel.read4ByteTxRx(port_num1, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_PRESENT_POSITION)
        # 다이나믹셀에서 현재 위치 정보를 읽어오는 함수 호출 dxl1_present_position 변수에 할당

        if dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION) != COMM_SUCCESS:
            # dynamixel.getLastTxRxResult()함수는 포트 번호와 프로토콜 버전을 인자로 받아 마지막으로 송수신된 결과를 반환
            # 마지막으로 송수신된 결과를 확인하여 통신이 성공했는지 확인

            dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION))
            # 통신이 성공하지 않았을 경우, 마지막으로 발생한 통신 오류를 출력하는 함수 호출

        elif dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION) != 0:
            # 만약 통신이 성공했지만, 수신된 패킷에 오류가 있다면 (0이 아니면)
            
            dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION))
            # 패킷 수신 오류를 출력하는 함수 호출, 프로토콜 버전과 패킷 오류를 받아 해당 오류를 출력

        # Read present position
        dxl2_present_position = dynamixel.read4ByteTxRx(port_num2, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
        if dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION) != COMM_SUCCESS:
            dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION))
        elif dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION) != 0:
            dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_goal_position[index], dxl2_present_position))

        # Dynamixel 서브 모터의 목표 위치와 현재 위치를 출력
        # ID : 현재 다이나믹셀 장치의 ID
        # GoalPos : 목표 위치 
        # PresPos : 현재 위치
        # %03d는 정수를 세 자리로 표시
        # DXL1_ID와 DXL2_ID는 각각 다이나믹셀 장치의 모터 ID
        # dxl_goal_position[index] 두 모터의 목표 위치

        if not ((abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD) or (abs(dxl_goal_position[index] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD)):
            break
        
        # abs(dxl_goal_position[index] - dxl1_present_position) =  다이나믹셀 1의 현재 위치와 목표 위치 간의 차이를 절댓값으로 계산
        # 다이나믹셀 1의 현재 위치와 목표 위치의 차이가 이동 상태 임계값(서브 모터가 움직이는지 여부를 판단하는 기준값)보다 큰지를 확인
        # 두 개의 Dynamixel 서보 모터의 목표 위치와 현재 위치의 차이가 `DXL_MOVING_STATUS_THRESHOLD`보다 작을 때 break문 실행

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


# Disable Dynamixel #1 Torque
dynamixel.write1ByteTxRx(port_num1, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)

# Dynamixel 서보 모터에 대해 토크를 비활성화하는 명령을 전송하는 역할
#`port_num1`은 Dynamixel과 연결된 포트의 번호
# PROTOCOL_VERSION은 사용 중인 프로토콜 버전 
# DXL1_ID`는 첫 번째 Dynamixel 서보 모터의 ID
# ADDR_PRO_TORQUE_ENABLE`은 토크를 제어하는 레지스터의 주소
# TORQUE_DISABLE`은 토크를 비활성화하는 값

if dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION) != COMM_SUCCESS:
    # 다이나믹셀과의 통신 결과가 성공적이지 않은 경우

    dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num1, PROTOCOL_VERSION))
    # 통신 결과가 성공적이지 않은 경우, 통신 오류를 출력하는 함수를 호출, 오류 코드는 PROTOCOL_VERSION과 함께 출력

elif dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION) != 0:
    # 통신은 성공했지만 수신된 패킷에 오류가 있는 경우를 확인

    dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num1, PROTOCOL_VERSION))
    #  오류 메시지를 출력 (PROTOCOL_VERSION과 함께 출력)

# Disable Dynamixel #2 Torque
dynamixel.write1ByteTxRx(port_num2, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION) != COMM_SUCCESS:
    dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num2, PROTOCOL_VERSION))
elif dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION) != 0:
    dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num2, PROTOCOL_VERSION))

# Close port
dynamixel.closePort(port_num1)
dynamixel.closePort(port_num2)

# 다이나믹셀과의 통신을 사용한 후 해당 포트를 종료하는 역할
# 다이나믹셀과의 연결을 해제

