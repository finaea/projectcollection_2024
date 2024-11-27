module Main where

import System.Random

data TreasureCount = IsTreasure | TreasureCount Int deriving Eq
instance Show TreasureCount where
  show IsTreasure = "T"
  show (TreasureCount n) = show n
instance Num TreasureCount where
  (-) (TreasureCount x) IsTreasure = TreasureCount (x - 1)
  (-) (TreasureCount x) (TreasureCount _) = TreasureCount x
  (-) _ _ = error "The (-) operation for data TreasureCount could not be conducted. Please complete the implementation."
  fromInteger = TreasureCount . fromIntegral

getValue :: TreasureCount -> Int
getValue IsTreasure = 1
getValue (TreasureCount i) = i

data TileState = Open | Close deriving (Show, Eq)

data Tile = Tile
  { nearestTreasure :: TreasureCount,
    state :: TileState
  }
  deriving (Show)
type Grid = [[Tile]]

data DiffSettings =  DiffSettings 
  { row :: Int,
    column :: Int,
    numTreasures :: TreasureCount
  }
diffBeginner = DiffSettings { row = 3 , column = 4, numTreasures = TreasureCount 4 }
diffIntermediate = DiffSettings { row = 4, column = 5, numTreasures = TreasureCount 8 }
diffExpert = DiffSettings { row = 6, column = 7, numTreasures = TreasureCount 12 }

data PlayerScore = PlayerScore 
  { name :: String,
    score :: Int
  } deriving (Show)
type Leaderboard = [PlayerScore]

-----------------------Editing Specific Tile---------------------------

replaceAtIndex :: Int -> a -> [a] -> [a]
replaceAtIndex index x xs = take (index - 1) xs ++ [x] ++ drop index xs

updateGrid :: Int -> Int -> a -> [[a]] -> [[a]]
updateGrid row column tile grid = replaceAtIndex row (replaceAtIndex column tile (grid !! (row - 1))) grid

getRecord row column key grid = key (grid !! (row - 1) !! (column - 1))

--------------Grid Creation with numbers and treasures-----------------

initializeGrid :: Int -> Int -> Grid
initializeGrid row column = replicate row (replicate column (Tile (TreasureCount 0) Close))

updateGridWithTreasure :: Int -> Int -> Int -> Grid -> IO Grid
updateGridWithTreasure _ _ 0 grid = pure grid
updateGridWithTreasure row column count grid = do
  randomRow <- randomRIO (1, row)
  randomColumn <- randomRIO (1, column)
  if getRecord randomRow randomColumn nearestTreasure grid == IsTreasure
    then updateGridWithTreasure row column count grid
    else updateGridWithTreasure row column (count - 1) (updateGrid randomRow randomColumn (Tile {
         nearestTreasure = IsTreasure, state = Close}) grid)

------------------------------------------------------------------------

sliceTile :: Int -> [a] -> [a]
sliceTile index grid = drop (index - 2) $ take (index + 1) grid 

treasure3x3 :: Int -> Int -> Grid -> [Tile]
treasure3x3 row column grid =  mconcat $ sliceTile column <$> sliceTile row grid

countTreasure :: Int -> [Tile] -> Int
countTreasure count [] = count
countTreasure count (x:xs) 
  | nearestTreasure x == IsTreasure = countTreasure (count + 1) xs
  | otherwise = countTreasure count xs

updateGridWithNumbers :: Int -> Int -> [[Tile]] -> [[Tile]]
updateGridWithNumbers 0 _ grid = grid
updateGridWithNumbers row 0 grid = updateGridWithNumbers (row - 1) (length $ head grid) grid
updateGridWithNumbers row column grid 
  | getRecord row column nearestTreasure grid == IsTreasure = updateGridWithNumbers row (column - 1) grid
  | otherwise = updateGridWithNumbers row (column - 1) (updateGrid row column Tile {
  nearestTreasure = TreasureCount $ countTreasure 0 (treasure3x3 row column grid),
  state = Close
} grid)

-------------------------In Game Display--------------------------------

displayGrid :: Int -> Int -> Grid -> IO ()
displayGrid 0 _ grid = do
  return ()
displayGrid row 0 grid = do
  putStrLn ""
  displayGrid (row - 1) (length $ head grid) grid
displayGrid row column grid = do
  if getRecord row column state grid == Close
    then putStr "[X] "
    else putStr ("[" ++ (show $ getRecord row column nearestTreasure grid) ++ "] ") 
  displayGrid row (column - 1) grid

initializeGame :: DiffSettings -> IO Grid
initializeGame diff = do
  let mr = row diff
      mc = column diff
      t = getValue (numTreasures diff)
  grid <- updateGridWithTreasure mr mc t (initializeGrid mr mc)
  pure $ updateGridWithNumbers mr mc grid

-- validateInput :: Int -> Int -> Grid -> IO Bool
validateInput row column grid
 | row < 1 || row > length grid = putStrLn "WARNING!! Wrong row input or row out of bound!" >> return False
 | column < 1 || column > (length $ head grid) = putStrLn "WARNING!! Wrong column input or column out of bound!" >> return False
 | getRecord row column state grid == Open = putStrLn "WARNING!! Tile has already opened!" >> return False
 | otherwise = return True

game :: Leaderboard -> DiffSettings -> TreasureCount -> Int -> Grid -> IO Leaderboard
game leaderboard diff 0 steps grid = do
  let mr = row diff
      mc = column diff
  putStrLn "=============================================="
  putStrLn "Congratulations! You found all the treasures!"
  putStrLn ""
  displayGrid mr mc (reverse <$> reverse grid)
  putStrLn ""
  putStrLn ("Your step count is " ++ show steps ++ "!")
  putStrLn ""
  putStrLn "Please enter the name you like to register"
  putStrLn "for the Leaderboard:"
  n <- getLine
  putStrLn "=============================================="
  putStrLn "Registed! You will be proceed back to the Menu."
  return $ leaderboard <> [PlayerScore { name = n, score = steps }]
game leaderboard diff treasureCount steps grid = do
  let mr = row diff
      mc = column diff
  putStrLn "=============================================="
  putStrLn ("Game has started with "++ show mr ++ " x "++ show mc ++ " grid board!")
  putStrLn ("Current Steps: " ++ show steps ++ "    Treasures Left: " ++ show treasureCount)
  putStrLn ""
  displayGrid mr mc (reverse <$> reverse grid)
  putStrLn ""
  putStrLn "Enter the row: "
  inputRow <- getLine
  let ir = read inputRow
  putStrLn "Enter the column: "
  inputColumn <- getLine
  let ic = read inputColumn
  putStrLn "=============================================="
  validated <- validateInput ir ic grid
  if validated == False
    then game leaderboard diff treasureCount steps grid
    else game leaderboard diff (treasureCount - (getRecord ir ic nearestTreasure grid)) (steps + 1) (updateGrid ir ic Tile {
      nearestTreasure = getRecord ir ic nearestTreasure grid,
      state = Open
      } grid)

-----------------------------Menu Display--------------------------------

displayMenu :: Leaderboard -> IO String
displayMenu leaderboard = do
  putStrLn "=============================================="
  putStrLn " Welcome to the Treasure Sweep Game!          "
  putStrLn " 1. Play Game                                 "
  putStrLn " 2. Tutorial                                  "
  putStrLn " 3. Leaderboard                               "
  putStrLn " 4. Exit                                      "
  putStrLn "=============================================="
  getLine >>= menuProcess leaderboard

displayTutorial :: IO ()
displayTutorial = do
  putStrLn "==========================================================="
  putStrLn "The treasures will be scattered around the grid            "
  putStrLn "and you will have to guess the location of the             "
  putStrLn "treasures. All tiles will be closed at the start           "
  putStrLn "the game and can be opened to reveal the treasure or       "
  putStrLn "number. The symbols displayed on the tile means:           "
  putStrLn "                                                           "
  putStrLn "1 to 9 = number of treasures adjacent to the tile          "
  putStrLn "T = one treasure in this tile                              "
  putStrLn "X = tile is closed                                         "
  putStrLn "                                                           "
  putStrLn "State the row and column of the tile you want to           "
  putStrLn "open when prompted. Each opened tile considered one step.  "
  putStrLn "                                                           "
  putStrLn "Earn high score by finding all the treasures at            "
  putStrLn "the least steps!                                           "
  putStrLn "==========================================================="

displayLeaderboard :: Leaderboard -> IO ()
displayLeaderboard [] = do
  putStrLn "=============================================="
displayLeaderboard leaderboard = do
  putStrLn ("Player: " ++ (show . name . head $ leaderboard) ++ " , Steps: " ++ (show . score . head $ leaderboard))
  displayLeaderboard (drop 1 leaderboard)

difficultySelect :: IO String
difficultySelect = do
  putStrLn "=============================================="
  putStrLn " Select the difficulty for the game           "
  putStrLn " 1. Beginner (4 bombs)                        "
  putStrLn " 2. Intermediate (8 bombs)                    "
  putStrLn " 3. Expert (12 bombs)                         "
  putStrLn " 4. Back to Menu                              "
  putStrLn "=============================================="
  getLine

menuProcess :: Leaderboard -> String -> IO String
menuProcess leaderboard "1" = difficultySelect >>= gameProcess leaderboard
menuProcess leaderboard "2" = displayTutorial >> displayMenu leaderboard
menuProcess leaderboard "3" = putStrLn "==============================================\nLeaderboard\n" >> displayLeaderboard leaderboard >> displayMenu leaderboard
menuProcess leaderboard "4" = putStrLn "Program is closing. Press Enter to continue." >> getLine
menuProcess leaderboard _ = putStrLn "You have entered the wrong input. Please try again." >> displayMenu leaderboard

gameProcess :: Leaderboard -> String -> IO String
gameProcess leaderboard "1" = initializeGame diffBeginner >>= game leaderboard diffBeginner (numTreasures diffBeginner) 0 >>= displayMenu
gameProcess leaderboard "2" = initializeGame diffIntermediate >>= game leaderboard diffIntermediate (numTreasures diffIntermediate) 0 >>= displayMenu
gameProcess leaderboard "3" = initializeGame diffExpert >>= game leaderboard diffExpert (numTreasures diffExpert) 0 >>= displayMenu
gameProcess leaderboard "4" = displayMenu leaderboard
gameProcess leaderboard _ = putStrLn "You have entered the wrong input. Please try again." >> difficultySelect >>= gameProcess leaderboard

main :: IO String
main = displayMenu ([] :: Leaderboard)