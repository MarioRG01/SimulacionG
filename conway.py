"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
Alberto Morales Vizcarra
Mario Rodriguez Gonzalez
Raquel Ochoa Martinez
"""

import pygame
import sys
import copy
from GameOfLife import makeSim
import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LEFT_PANNEL_BACKGROUND_COLOR = (15,10,20)
RIGHT_PANNEL_BACKGROUND_COLOR = (50,12,120)
GRID_PANNEL_BACKGROUND_COLOR = (15,25,55)
TITLE_COLOR = (245,250,240)
START_BUTTON_COLOR = (5,105,5)
STOP_BUTTON_COLOR = (105,10,5)
START_BUTTON_TEXT_COLOR = WHITE
STOP_BUTTON_TEXT_COLOR = WHITE
LOAD_BUTTON_COLOR = (10,130,150)
LOAD_BUTTON_TEXT_COLOR = WHITE
CLEAR_BUTTON_COLOR = (255,75,75)
CLEAR_BUTTON_TEXT_COLOR = WHITE
GENERATIONS_COLOR = (15,245,100)
CONFIGURATIONS_COLOR = (200,240,40)
SCREEN_HEIGHT_COLOR = (230,180,40)
SCREEN_HEIGHT_INPUT_COLOR = (210,140,210)
SCREEN_HEIGHT_INPUT_EDIT_COLOR = (170,90,170)
SCREEN_HEIGHT_INPUT_TEXT_COLOR = WHITE
SCREEN_HEIGHT_TEXT_COLOR = WHITE
SCREEN_HEIGHT_RESIZE_BUTTON_COLOR = (20,20,145)
SCREEN_HEIGHT_RESIZE_BUTTON_TEXT_COLOR = WHITE
UNIVERSE_SIZE_COLOR = (120,250,200)
WIDTH_HEIGHT_LABELS_COLOR = (250,120,200)
WIDTH_HEIGHT_INPUT_COLOR = (180,150,250)
WIDTH_HEIGHT_INPUT_EDIT_COLOR = (140,115,200)
WIDTH_HEIGHT_INPUT_TEXT_COLOR = WHITE
UNIVERSE_SIZE_RESIZE_BUTTON_COLOR = (20,20,145)
UNIVERSE_SIZE_RESIZE_BUTTON_TEXT_COLOR = WHITE
GENERATIONS_COLOR = (40,205,90)
GENERATIONS_INPUT_COLOR = (60,190,130)
GENERATIONS_INPUT_EDIT_COLOR = (20,150,95)
GENERATIONS_INPUT_TEXT_COLOR = WHITE
ALIVE_CELL_COLOR = (144,12,63)
DEAD_CELL_COLOR = (228,228,140)
LABELS_COLOR = (200,200,200)
DATA_COLOR = (250,245,245)
HIGHLIGHT_COLOR = (200,200,200)
LOAD_ERROR_INDICATOR_COLOR = (255,0,0)

def lightenColor(rgb):
    red, green, blue = rgb
    newRed = min(255, int(red + 0.6 * (255 - red)))
    newGreen = min(255, int(green + 0.6 * (255 - green)))
    newBlue = min(255, int(blue + 0.6 * (255 - blue)))

    return (newRed, newGreen, newBlue)

def resizeGrid(grid, cols, rows):
    newGrid = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(min(len(grid), rows)):
        for j in range(min(len(grid[0]), cols)):
            newGrid[i][j] = grid[i][j]
    grid = copy.deepcopy(newGrid)
    return grid
def draw_grid(surface, grid, rows, cols, gridSize, widthOffset):
    cells = {}
    rowOffset = 0
    colOffset = 0
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]
    if cols < rows:
        colOffset = (rows - cols) / 2
    elif cols > rows:
        rowOffset = (cols - rows) / 2
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                cells[(row, col)] = pygame.draw.rect(surface, ALIVE_CELL_COLOR, ((col + colOffset) * gridWidth + widthOffset, (row + rowOffset) * gridHeight + rowOffset, gridWidth, gridHeight))
                pygame.draw.rect(surface, GRID_PANNEL_BACKGROUND_COLOR, ((col + colOffset) * gridWidth + widthOffset, (row + rowOffset) * gridHeight + rowOffset, gridWidth, gridHeight), 2)
            else:
                cells[(row, col)] = pygame.draw.rect(surface, DEAD_CELL_COLOR, ((col + colOffset) * gridWidth + widthOffset, (row + rowOffset) * gridHeight + rowOffset, gridWidth, gridHeight))
                pygame.draw.rect(surface, GRID_PANNEL_BACKGROUND_COLOR, ((col + colOffset) * gridWidth + widthOffset, (row + rowOffset) * gridHeight + rowOffset, gridWidth, gridHeight), 2)
    return cells

def drawLeftPannel(surface, screenHeight, width, height, grid, editing, screenHeightValue, universeWidthValue, universeHeightValue, simRunning, currentGeneration, generationsValue, loadError):
    pygame.draw.rect(surface, LEFT_PANNEL_BACKGROUND_COLOR, (0, 0, width, height))
    elements = {}
    # Title
    titleFontSize = int(width * 0.2)
    titleFont = pygame.font.Font(None, titleFontSize)
    titleTextField = titleFont.render("Game of Life", True, TITLE_COLOR)
    titleX = width * 0.01
    titleY = height * 0.01 
    
    # Buttons Font
    buttonFontSize = int(width * 0.1)
    buttonFont = pygame.font.Font(None, buttonFontSize)

    # Start Button
    startButtonX = width * 0.02
    startButtonY = height * 0.1
    startButtonWidth = width * 0.8
    startButtonHeight = height * 0.06
    startButton = pygame.Rect(startButtonX, startButtonY, startButtonWidth, startButtonHeight)
    startButtonText = buttonFont.render("Start", True, START_BUTTON_TEXT_COLOR)
    elements["startButton"] = startButton
    
    # Load Button
    loadConfButtonX = startButtonX
    loadConfButtonY = startButtonY * 1.2 + startButtonHeight
    loadConfButtonWidth = startButtonWidth * 0.5
    loadConfButtonHeight = startButtonHeight * 0.8
    loadConfButton = pygame.Rect(loadConfButtonX, loadConfButtonY, loadConfButtonWidth, loadConfButtonHeight)
    loadConfButtonText = buttonFont.render("Load", True, LOAD_BUTTON_TEXT_COLOR)
    elements["loadConfButton"] = loadConfButton
    
    # Load Error Indicator
    loadErrorIndicatorX = loadConfButtonX + loadConfButtonWidth
    loadErrorIndicatorY = loadConfButtonY
    loadErrorIndicatorRadius = loadConfButtonWidth * 0.05
    
    # Clear Button
    clearButtonX = loadConfButtonX + loadConfButtonWidth * 1.4
    clearButtonY = startButtonY * 1.2 + startButtonHeight
    clearButtonWidth = startButtonWidth * 0.3
    clearButtonHeight = startButtonHeight * 0.8
    clearButton = pygame.Rect(clearButtonX, clearButtonY, clearButtonWidth, clearButtonHeight)
    clearButtonText = buttonFont.render("Clear", True, CLEAR_BUTTON_TEXT_COLOR)
    elements["clearButton"] = clearButton
    
    # Generation Counter
    generationCounterFontSize = int(width * 0.09)
    generationCounterFont = pygame.font.Font(None, generationCounterFontSize)
    generationCounterTextField = generationCounterFont.render("Generation: " + str(currentGeneration), True, GENERATIONS_COLOR)
    generationCounterX = width * 0.2
    generationCounterY = loadConfButtonY * 1.15 + loadConfButtonHeight
    
    # Configuration
    confFontSize = int(width * 0.15)
    confFont = pygame.font.Font(None, confFontSize)
    confTextField = confFont.render("Configurations", True, CONFIGURATIONS_COLOR)
    confX = titleX
    confY = generationCounterY * 1.2
    
    # Screen Height Label
    screenHeightLabelFontSize = int(width * 0.1)
    screenHeightLabelFont = pygame.font.Font(None, screenHeightLabelFontSize)
    screenHeightLabelTextField = screenHeightLabelFont.render("Screen Height", True, SCREEN_HEIGHT_TEXT_COLOR)
    screenHeightLabelX = width * 0.08
    screenHeightLabelY = confY * 1.2
    
    # Screen Height Input
    screenHeightInputX = screenHeightLabelX
    screenHeightInputY = screenHeightLabelY * 1.08
    screenHeightInputWidth = width * 0.4
    screenHeightInputHeight = height * 0.03
    screenHeightInput = pygame.Rect(screenHeightInputX, screenHeightInputY, screenHeightInputWidth, screenHeightInputHeight)
    screenHeightInputTextValue = str(screenHeightValue)
    screenHeightInputFontSize = int(width * 0.08)
    screenHeightInputFont = pygame.font.Font(None, screenHeightInputFontSize)
    screenHeightInputText = screenHeightInputFont.render(screenHeightInputTextValue, True, SCREEN_HEIGHT_INPUT_TEXT_COLOR)
    elements["screenHeightInput"] = screenHeightInput
    
    # Screen Height Resize Button
    screenHeightResizeButtonX = screenHeightInputX * 1.5 + screenHeightInputWidth
    screenHeightResizeButtonY = screenHeightInputY
    screenHeightResizeButtonWidth = screenHeightInputWidth * 0.8
    screenHeightResizeButtonHeight = screenHeightInputHeight
    screenHeightResizeButton = pygame.Rect(screenHeightResizeButtonX, screenHeightResizeButtonY, screenHeightResizeButtonWidth, screenHeightResizeButtonHeight)
    screenHeightResizeButtonFontSize = int(width * 0.08)
    screenHeightResizeButtonFont = pygame.font.Font(None, screenHeightResizeButtonFontSize)
    screenHeightResizeButtonText = screenHeightResizeButtonFont.render("Resize", True, SCREEN_HEIGHT_RESIZE_BUTTON_TEXT_COLOR)
    elements["screenHeightResizeButton"] = screenHeightResizeButton
    
    # Universe Size
    universeSizeFontSize = int(width * 0.1)
    universeSizeFont = pygame.font.Font(None, universeSizeFontSize)
    universeSizeTextField = universeSizeFont.render("Universe Size", True, UNIVERSE_SIZE_COLOR)
    universeSizeX = screenHeightInputX
    universeSizeY = screenHeightInputY * 1.1 + screenHeightInputHeight
    
    # Universe Width Label
    universeWidthLabelFontSize = int(width * 0.08)
    universeWidthLabelFont = pygame.font.Font(None, universeWidthLabelFontSize)
    universeWidthLabelTextField = universeWidthLabelFont.render("Width", True, WIDTH_HEIGHT_LABELS_COLOR)
    universeWidthLabelX = universeSizeX * 1.4
    universeWidthLabelY = universeSizeY * 1.1
    
    # Universe Width Input
    universeWidthInputX = universeWidthLabelX
    universeWidthInputY = universeWidthLabelY * 1.05
    universeWidthInputWidth = width * 0.35
    universeWidthInputHeight = height * 0.025
    universeWidthInput = pygame.Rect(universeWidthInputX, universeWidthInputY, universeWidthInputWidth, universeWidthInputHeight)
    universeWidthInputTextValue = str(universeWidthValue)
    universeWidthInputFontSize = int(width * 0.075)
    universeWidthInputFont = pygame.font.Font(None, universeWidthInputFontSize)
    universeWidthInputText = universeWidthInputFont.render(universeWidthInputTextValue, True, WIDTH_HEIGHT_INPUT_TEXT_COLOR)
    elements["universeWidthInput"] = universeWidthInput
    
    # Universe Height Label
    universeHeightLabelFontSize = int(width * 0.08)
    universeHeightLabelFont = pygame.font.Font(None, universeHeightLabelFontSize)
    universeHeightLabelTextField = universeHeightLabelFont.render("Height", True, WIDTH_HEIGHT_LABELS_COLOR)
    universeHeightLabelX = universeSizeX * 1.4
    universeHeightLabelY = universeWidthInputY * 1.02 + universeWidthInputHeight
    
    # Universe Height Input
    universeHeightInputX = universeHeightLabelX
    universeHeightInputY = universeHeightLabelY * 1.05
    universeHeightInputWidth = width * 0.35
    universeHeightInputHeight = height * 0.025
    universeHeightInput = pygame.Rect(universeHeightInputX, universeHeightInputY, universeHeightInputWidth, universeHeightInputHeight)
    universeHeightInputTextValue = str(universeHeightValue)
    universeHeightInputFontSize = int(width * 0.075)
    universeHeightInputFont = pygame.font.Font(None, universeHeightInputFontSize)
    universeHeightInputText = universeHeightInputFont.render(universeHeightInputTextValue, True, WIDTH_HEIGHT_INPUT_TEXT_COLOR)
    elements["universeHeightInput"] = universeHeightInput
    
    # Resize Universe Button
    resizeUniverseButtonX = screenHeightResizeButtonX
    resizeUniverseButtonY = universeWidthInputY + universeWidthInputHeight
    resizeUniverseButtonWidth = screenHeightResizeButtonWidth
    resizeUniverseButtonHeight = height * 0.03
    resizeUniverseButton = pygame.Rect(resizeUniverseButtonX, resizeUniverseButtonY, resizeUniverseButtonWidth, resizeUniverseButtonHeight)
    resizeUniverseButtonFontSize = int(width * 0.075)
    resizeUniverseButtonFont = pygame.font.Font(None, resizeUniverseButtonFontSize)
    resizeUniverseButtonText = resizeUniverseButtonFont.render("Resize", True, UNIVERSE_SIZE_RESIZE_BUTTON_TEXT_COLOR)
    elements["resizeUniverseButton"] = resizeUniverseButton
    
    # Set Generations Label
    generationsLabelFontSize = universeSizeFontSize
    generationsLabelFont = pygame.font.Font(None, generationsLabelFontSize)
    generationsLabelTextField = generationsLabelFont.render("Generations", True, GENERATIONS_COLOR)
    generationsLabelX = universeSizeX
    generationsLabelY = universeHeightInputY * 1.05 + universeHeightInputHeight
    
    # Set Generations Input
    generationsInputX = generationsLabelX
    generationsInputY = generationsLabelY * 1.05
    generationsInputWidth = width * 0.4
    generationsInputHeight = height * 0.03
    generationsInput = pygame.Rect(generationsInputX, generationsInputY, generationsInputWidth, generationsInputHeight)
    generationsInputTextValue = str(generationsValue)
    generationsInputFontSize = int(width * 0.08)
    generationsInputFont = pygame.font.Font(None, generationsInputFontSize)
    generationsInputText = generationsInputFont.render(generationsInputTextValue, True, GENERATIONS_INPUT_TEXT_COLOR)
    elements["generationsInput"] = generationsInput
    
    # Draw text fields
    surface.blit(titleTextField, (titleX, titleY))
    surface.blit(confTextField, (confX, confY))
    surface.blit(screenHeightLabelTextField, (screenHeightLabelX, screenHeightLabelY))
    surface.blit(universeSizeTextField, (universeSizeX, universeSizeY))
    surface.blit(universeWidthLabelTextField, (universeWidthLabelX, universeWidthLabelY))
    surface.blit(universeHeightLabelTextField, (universeHeightLabelX, universeHeightLabelY))
    surface.blit(generationCounterTextField, (generationCounterX, generationCounterY))
    surface.blit(generationsLabelTextField, (generationsLabelX, generationsLabelY))
    
    # Draw buttons
    if simRunning:
        pygame.draw.rect(surface, STOP_BUTTON_COLOR, startButton)
        startButtonText = buttonFont.render("Stop", True, STOP_BUTTON_TEXT_COLOR)
    elif editing == "startButton":
        pygame.draw.rect(surface, START_BUTTON_COLOR, startButton)
    else:
        pygame.draw.rect(surface, START_BUTTON_COLOR, startButton)
    surface.blit(startButtonText, (startButtonX + (startButtonWidth - startButtonText.get_width()) // 2, startButtonY + (startButtonHeight - startButtonText.get_height()) // 2))
    
    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), loadConfButton)
    elif editing == "loadConfButton":
        pygame.draw.rect(surface, lightenColor(LOAD_BUTTON_COLOR), loadConfButton)
    else:
        pygame.draw.rect(surface, LOAD_BUTTON_COLOR, loadConfButton)
    surface.blit(loadConfButtonText, (loadConfButtonX + (loadConfButtonWidth - loadConfButtonText.get_width()) // 2, loadConfButtonY + (loadConfButtonHeight - loadConfButtonText.get_height()) // 2))
    
    if loadError:
        pygame.draw.circle(surface, LOAD_ERROR_INDICATOR_COLOR, (loadErrorIndicatorX, loadErrorIndicatorY), loadErrorIndicatorRadius)

    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), clearButton)
    elif editing == "clearButton":
        pygame.draw.rect(surface, lightenColor(CLEAR_BUTTON_COLOR), clearButton)
    else:
        pygame.draw.rect(surface, CLEAR_BUTTON_COLOR, clearButton)
    surface.blit(clearButtonText, (clearButtonX + (clearButtonWidth - clearButtonText.get_width()) // 2, clearButtonY + (clearButtonHeight - clearButtonText.get_height()) // 2))
    
    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), screenHeightInput)
    elif editing == "screenHeightInput":
        pygame.draw.rect(surface, SCREEN_HEIGHT_INPUT_EDIT_COLOR, screenHeightInput)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, screenHeightInput, 2)
    else:
        pygame.draw.rect(surface, SCREEN_HEIGHT_INPUT_COLOR, screenHeightInput)
    surface.blit(screenHeightInputText, (screenHeightInputX + (screenHeightInputWidth - screenHeightInputText.get_width()) // 2, screenHeightInputY + (screenHeightInputHeight - screenHeightInputText.get_height()) // 2))
    
    if simRunning or screenHeightValue == 0:
        pygame.draw.rect(surface, (125, 125, 125), screenHeightResizeButton)
    elif editing == "screenHeightResizeButton":
        pygame.draw.rect(surface, lightenColor(SCREEN_HEIGHT_RESIZE_BUTTON_COLOR), screenHeightResizeButton)
    else:
        pygame.draw.rect(surface, SCREEN_HEIGHT_RESIZE_BUTTON_COLOR, screenHeightResizeButton)
    surface.blit(screenHeightResizeButtonText, (screenHeightResizeButtonX + (screenHeightResizeButtonWidth - screenHeightResizeButtonText.get_width()) // 2, screenHeightResizeButtonY + (screenHeightResizeButtonHeight - screenHeightResizeButtonText.get_height()) // 2))
    
    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), universeWidthInput)
    elif editing == "universeWidthInput":
        pygame.draw.rect(surface, WIDTH_HEIGHT_INPUT_EDIT_COLOR, universeWidthInput)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, universeWidthInput, 2)
    else:
        pygame.draw.rect(surface, WIDTH_HEIGHT_INPUT_COLOR, universeWidthInput)
    surface.blit(universeWidthInputText, (universeWidthInputX + (universeWidthInputWidth - universeWidthInputText.get_width()) // 2, universeWidthInputY + (universeWidthInputHeight - universeWidthInputText.get_height()) // 2))
    
    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), universeHeightInput)
    elif editing == "universeHeightInput":
        pygame.draw.rect(surface, WIDTH_HEIGHT_INPUT_EDIT_COLOR, universeHeightInput)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, universeHeightInput, 2)

    else:
        pygame.draw.rect(surface, WIDTH_HEIGHT_INPUT_COLOR, universeHeightInput)
    surface.blit(universeHeightInputText, (universeHeightInputX + (universeHeightInputWidth - universeHeightInputText.get_width()) // 2, universeHeightInputY + (universeHeightInputHeight - universeHeightInputText.get_height()) // 2))
    
    if simRunning or universeWidthValue == 0 or universeHeightValue == 0:
        pygame.draw.rect(surface, (125, 125, 125), resizeUniverseButton)
    elif editing == "resizeUniverseButton":
        pygame.draw.rect(surface, lightenColor(UNIVERSE_SIZE_RESIZE_BUTTON_COLOR), resizeUniverseButton)
    else:
        pygame.draw.rect(surface, UNIVERSE_SIZE_RESIZE_BUTTON_COLOR, resizeUniverseButton)
    surface.blit(resizeUniverseButtonText, (resizeUniverseButtonX + (resizeUniverseButtonWidth - resizeUniverseButtonText.get_width()) // 2, resizeUniverseButtonY + (resizeUniverseButtonHeight - resizeUniverseButtonText.get_height()) // 2))
    
    if simRunning:
        pygame.draw.rect(surface, (125, 125, 125), generationsInput)
    elif editing == "generationsInput":
        pygame.draw.rect(surface, GENERATIONS_INPUT_EDIT_COLOR, generationsInput)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, generationsInput, 2)
    else:
        pygame.draw.rect(surface, GENERATIONS_INPUT_COLOR, generationsInput)
    surface.blit(generationsInputText, (generationsInputX + (generationsInputWidth - generationsInputText.get_width()) // 2, generationsInputY + (generationsInputHeight - generationsInputText.get_height()) // 2))
    
    return elements
def drawRightPannel(surface, x, y, width, height, entities):
    pygame.draw.rect(surface, RIGHT_PANNEL_BACKGROUND_COLOR, (x, y, width, height))
    # Labels
    labelsFontSize = int(width * 0.1)
    labelsFont = pygame.font.Font(None, labelsFontSize)
    # Name Label
    nameLabelTextField = labelsFont.render("Name", True, LABELS_COLOR)
    nameLabelX = x + width * 0.15
    nameLabelY = height * 0.03
    # Count Label
    countLabelTextField = labelsFont.render("Count", True, LABELS_COLOR)
    countLabelX = nameLabelX * 1.07
    countLabelY = nameLabelY
    # Percentage Label
    percentageLabelTextField = labelsFont.render("%", True, LABELS_COLOR)
    percentageLabelX = countLabelX * 1.07
    percentageLabelY = nameLabelY 
    
    surface.blit(nameLabelTextField, (nameLabelX, nameLabelY))
    surface.blit(countLabelTextField, (countLabelX, countLabelY))
    surface.blit(percentageLabelTextField, (percentageLabelX, percentageLabelY))
    
    totalEntities = sum(entities.values())
    
    entitiesData = []
    
    # Entities
    entitiesFontSize = int(width * 0.1)
    entitiesFont = pygame.font.Font(None, entitiesFontSize)
    py = height // 12
    c = 0
    for entity in entities:
        name = entity
        if name == "lightWeightSpaceship":
            name = "LWSShip"
        count = entities[entity]
        if totalEntities == 0:
            percentage = 0.0
        else:
            percentage = round(count / totalEntities * 100,2)
        nameTextField = entitiesFont.render(name, True, DATA_COLOR)
        countTextField = entitiesFont.render(str(count), True, DATA_COLOR)
        percentageTextField = entitiesFont.render(str(percentage) + "%", True, DATA_COLOR)
        posX = nameLabelX
        posY = py * (c+1)
        e = [nameTextField, countTextField, percentageTextField, posX, posY]
        entitiesData.append(e)
        surface.blit(nameTextField, (posX, posY))
        surface.blit(countTextField, (posX * 1.09, posY))
        surface.blit(percentageTextField, (posX * 1.09 * 1.045, posY))
        c += 1

def main(screenHeight, grid, rows, cols, generations, currentGeneration, entities):
    widthHeightRatio = 1.2
    
    gridWidth = screenHeight * widthHeightRatio
    gridHeight = screenHeight
    
    cellWidth = gridWidth / max(rows, cols)
    cellHeight = gridHeight / max(rows, cols)
    
    gridSize = [cellWidth, cellHeight]

    pannelsRatio = 0.3
    
    leftPannelWidth = gridWidth * pannelsRatio
    leftPannelHeight = screenHeight
    
    rightPannelWidth = gridWidth * pannelsRatio
    rightPannelHeight = screenHeight
    
    editingScreenHeight = False
    editingUniverseWidth = False
    editingUniverseHeight = False
    editingGenerations = False
    
    tempScreenHeight = screenHeight
    
    tempUniverseRows = rows
    tempUniverseCols = cols
    
    clickAction = ""
    
    universeWidthValue = len(grid[0])
    universeHeightValue = len(grid)
    
    generationsValue = generations
    
    cellsGrid = []
    
    simRunning = False

    endWindow = False
    
    outputFileName = ""
    
    loadError = False