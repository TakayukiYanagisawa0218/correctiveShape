# -*- coding: utf-8 -*-
'''
-----------------------------------------------------------------------------------
AUTHOR:		Takayuki Yanagisawa
			ty.null0218@gmail.com

Example usage:
import correctiveShape
correctiveShape.execute('deformObj', 'scluptObj')
or
correctiveShape.execute('deformObj', 'scluptObj', 'resultShapeName')
-----------------------------------------------------------------------------------
'''
from maya.api import OpenMaya as api
from maya import OpenMaya as om
from maya import cmds
import math

def isShapeError(nodeName):
	if not cmds.objectType(nodeName) == 'mesh':
		return True
	else:
		return False

def getOrigShape(objName):
	for shapeName in cmds.listRelatives(objName, c=1, s=1):
		if cmds.getAttr('%s.io'%shapeName):
			return shapeName
	return None

def getPosList(shapeName, space=api.MSpace.kObject):
	selList = api.MSelectionList()
	selList.add(shapeName)
	meshFn = api.MFnMesh(selList.getDagPath(0))
	return meshFn.getPoints(space)

def setPosList(shapeName, posList, space=api.MSpace.kObject):
	selList = api.MSelectionList()
	selList.add(shapeName)
	meshFn = api.MFnMesh(selList.getDagPath(0))	
	meshFn.setPoints(posList, space)

def offsetPosList(posList, offset=[0, 0, 0]):
	rltArray = api.MPointArray()
	for i in xrange(posList.__len__()):
		x = posList[i].x + offset[0]
		y = posList[i].y + offset[1]
		z = posList[i].z + offset[2]
		w = 1
		rltArray.append(api.MPoint(x, y, z, w))
	return rltArray

def setMatrixRow(matrix, newVector, row):
	setMatrixCell(matrix, newVector.x, row, 0)
	setMatrixCell(matrix, newVector.y, row, 1)
	setMatrixCell(matrix, newVector.z, row, 2)

def setMatrixCell(matrix, value, row, column):
	om.MScriptUtil.setDoubleArray(matrix[row], column, value)

def execute(deformObj, scluptObj, name='resultCorrective'):
	# get necessary shape names
	deformShape	= cmds.listRelatives(deformObj, c=1, s=1)[0]
	scluptShape	= cmds.listRelatives(scluptObj, c=1, s=1)[0]
	origShape	= getOrigShape(deformObj)
	for checkStr, shapeName in zip(['deformShape', 'scluptShape', 'origShape'],
		[deformShape, scluptShape, origShape]):
		if not shapeName:
			cmds.error('%s is not exists.'%checkStr)
		if isShapeError(shapeName):
			cmds.error('%s is not match type.'%shapeName)

	# create result object
	rlt			= cmds.createNode('transform', n=name)
	rltShape	= cmds.createNode('mesh', n=rlt + 'Shape', p=rlt)
	cmds.connectAttr(origShape + '.outMesh', rltShape + '.inMesh')
	cmds.sets(rltShape, e=1, fe='initialShadingGroup')

	# get vertex position (object space)
	origPos		= getPosList(origShape)
	deformPos	= getPosList(deformShape)
	scluptPos	= getPosList(scluptShape)
	
	# get number of vertices
	numPoints	= origPos.__len__()
	
	# offset vertex position
	origxPos	= offsetPosList(origPos, [1, 0, 0])
	origyPos	= offsetPosList(origPos, [0, 1, 0])
	origzPos	= offsetPosList(origPos, [0, 0, 1])
	
	# edit orig shape and get deformed position
	setPosList(origShape, origxPos)
	xPos = getPosList(deformShape)
	setPosList(origShape, origyPos)
	yPos = getPosList(deformShape)
	setPosList(origShape, origzPos)
	zPos = getPosList(deformShape)
	
	setPosList(origShape, origPos)
	
	# calculate vertex matrix for deformed position (nearly normalize vector)
	matrixArray = om.MMatrixArray()
	for i in xrange(numPoints):
		matrix = om.MMatrix()
		setMatrixRow(matrix, xPos[i] - deformPos[i], 0)
		setMatrixRow(matrix, yPos[i] - deformPos[i], 1)
		setMatrixRow(matrix, zPos[i] - deformPos[i], 2)
		matrixArray.append(matrix.inverse())
	
	# calculate target position (vertex local space)
	tolerance	= 1.0e-3
	rltArray	= api.MPointArray()
	for i in xrange(numPoints):
		delta = scluptPos[i] - deformPos[i]
		if (math.fabs(delta.x) < tolerance and math.fabs(delta.y) < tolerance and math.fabs(delta.z) < tolerance):
			point = api.MPoint(origPos[i].x, origPos[i].y, origPos[i].z)
		else:
			point = om.MPoint(delta.x, delta.y, delta.z) * matrixArray[i]
			point = api.MPoint(point.x + origPos[i].x, point.y + origPos[i].y, point.z + origPos[i].z)
		rltArray.append(point)
	
	setPosList(rltShape, rltArray)
	cmds.select(rlt)
	print '// Result: %s //'%rlt
	return rlt