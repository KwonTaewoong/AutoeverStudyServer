import numpy as np
import requests
import sys

def main():
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
	greed = CreateGreed(greedSize)
	greed = SetObstacleOnGreed(greed, obstacle)


def CreateGreed(greedSize):
	greed = np.zeros((greedSize, greedSize))
	return greed


def SetObstacleOnGreed(greed, obstacle):
	temp = greed[1:len(greed)-1,:]
	originShape = temp.shape
	temp = temp.ravel()
	index = np.random.choice(temp.shape[0], obstacle, False)
	for i in index:
		temp[i] = 1
	temp = temp.reshape(originShape)
	greed[1:len(greed)-1, :] = temp
	print(greed)

	return greed


if __name__ == "__main__":
	main()