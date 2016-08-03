import sys

nFunc = sys.argv[1]
sPass = sys.argv[2]

def CCDecrypt(sCCNum):
	nSeed = 9
	nPos = -1
	tmpSeed = nSeed
	sDecrypted = ''
	sCharAscii = ''
	sCharOffset = 0
	sNewChar = ''

	for sChar in sCCNum:
		nPos = nPos + 1
		if nPos == 0 or nPos == len(sCCNum) - 1:
			tmpSeed = nSeed

		#print sChar
		sCharAscii = ord(sChar)
		sCharOffset = sCharAscii - 18

		#print "Char: " + sChar + " Ascii: " + str(sCharAscii) + " Offset: " + str(sCharOffset)

		sNewChar = int(sCharOffset) ^ int(tmpSeed)
		#print str(sNewChar)
		if sNewChar > 47:
			sDecrypted = sDecrypted + chr(sNewChar)
		else:
			sNewChar = int(sNewChar) + 18
			sDecrypted = sDecrypted + chr(sNewChar)

		tmpSeed = sNewChar

	return sDecrypted

def CCEncrypt(sCCNum):
	nSeed = 9
	nPos = -1
	tmpSeed = nSeed
	sEncrypted = ''
	sCharAscii = ''
	sCharOffset = 0
	sNewChar = ''

	for sChar in sCCNum:
		nPos = nPos + 1
		if nPos == 0 or nPos == len(sCCNum) - 1:
			tmpSeed = nSeed

		#print sChar
		sCharAscii = ord(sChar)
		#sCharOffset = sCharAscii + 18

		print "-----------------------------"
		print "Char: " + sChar
		print "Ascii: " + str(sCharAscii)
		#print "Offset: " + str(sCharOffset)

		sNewChar = (int(sCharAscii) ^ int(tmpSeed)) + 18
		print "NC: " + str(sNewChar)

		if sNewChar < 256:
			sEncrypted = sEncrypted + chr(sNewChar)
		else:
			sNewChar = int(sNewChar) - 18
			print "Adj: " + chr(sNewChar)
			sEncrypted = sEncrypted + chr(sNewChar)

		tmpSeed = sNewChar
		print "Seed: " + str(tmpSeed)

	return sEncrypted

nFunc = nFunc.lower()

if nFunc.startswith("e") == True:
	sOut = CCEncrypt(sPass)
	print "Encrypted: " + str(sOut)

	sOut = CCDecrypt(sOut)
	print "Decrypted: " + str(sOut)


if nFunc.startswith("d") == True:
	sPass = "L!!P"   #378118078115007

	sOut = CCDecrypt(sPass)
	print "Decrypted: " + str(sOut)

	sOut = CCEncrypt(sOut)
	print "Encrypted: " + str(sOut)


