import numpy as np
import sys
import datetime
from simple_websocket_server import WebSocketServer, WebSocket




def main():

#웹 소켓 구현 부분
	class SimpleEcho(WebSocket):
		greed = None
		obstacle = None
		socketLog = None


		def SetData(Greed, Obstacle, SocketLog):
			greed = Greed
			obstacle = Obstacle
			socketLog = SocketLog



		def handle(self):

			if (self.data == "GetGreed"):
				self.send_message("greed:"+str(len(greed)))
			elif (self.data == "GetObs"):
				self.send_message(str(obstacle))
			elif (self.data == "GetAllGreed"):
				print(str(greed))
				self.send_message("getAllGreed:"+str(greed))
			elif "GetObjectRoot" in self.data:
				dataList = self.data.split(',')
				currentX = int(dataList[3])
				currentY = len(greed) - 1
				size = len(greed) - 1
				destX = int(dataList[2])
				destY = 0

				print(greed[currentY, currentX])
				root = []
				
				#rule based에 의한 시뮬레이션 영역
				while(True):
					if (greed[currentY-1, currentX] != 1 and currentY != 0):
						currentY = currentY-1
						root.append([currentX, currentY])
					else:
						if (currentX > destX):
							if (currentX == 0):
								currentX = currentX+1
								root.append([currentX, currentY])

							else:
								if (greed[currentY, currentX-1] != 1):
									currentX = currentX-1
									root.append([currentX, currentY])

								else:
									currentX = currentX+1
									root.append([currentX, currentY])

						else:
							if (currentX == size):
								currentX = currentX-1
								root.append([currentX, currentY])

							else:
								if (greed[currentY, currentX+1] != 1):
									currentX = currentX+1
									root.append([currentX, currentY])

								else:
									currentX = currentX-1
									root.append([currentX, currentY])

					if (currentX == destX and currentY == destY):
						break

				self.send_message("getRoot:"+dataList[1]+":"+str(root))

			#로깅 영역
			elif "objectID" in self.data:

				socketLog.write(self.data)


		def connected(self):
			print(self.address, 'connected')

		def handle_close(self):
			print(self.address, 'closed')


#잘못된 input 파라미터에 대한 반환 부분
	if len(sys.argv) != 3:
		print ("argument size is not 2")
		exit()

	if not sys.argv[1].isdecimal():
		print("input only number(arg1)")
		exit()

	if not sys.argv[2].isdecimal():
		print("input only number(arg2)")
		exit()

	greedSize = int(sys.argv[1])
	obstacle = int(sys.argv[2])

	if greedSize > 20 or greedSize < 5:
		print ("input greed size between 5 to 20")
		exit()

	if obstacle < 1 or obstacle > greedSize - 1:
		print ("obstacle is smaller than greedSize")
		exit()


#그리드 형성
	greed = CreateGreed(greedSize)
	socketLog = open("logFile.txt", 'a')

	greed = SetObstacleOnGreed(greed, obstacle)
	print("=======Map======")
	print(greed)


	server = WebSocketServer('localhost', 3000, SimpleEcho)
	SimpleEcho.SetData(greed, obstacle, socketLog)

	server.serve_forever()


def CreateGreed(greedSize):
	greed = np.zeros((greedSize, greedSize))
	return greed

#차원 변경을 통한 장애물 랜덤 배치 함수
def SetObstacleOnGreed(greed, obstacle):
	temp = greed[1:len(greed)-1,:]
	originShape = temp.shape
	temp = temp.ravel()
	index = np.random.choice(temp.shape[0], obstacle, False)
	for i in index:
		temp[i] = 1
	temp = temp.reshape(originShape)
	greed[1:len(greed)-1, :] = temp


	return greed


if __name__ == "__main__":
	main()