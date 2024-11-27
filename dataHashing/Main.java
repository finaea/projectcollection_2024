import java.util.Scanner;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Set;
import java.util.HashSet;

public class Main {
  public static final Hashtable<String, Integer> dictionary = new Hashtable<String, Integer>();

  static {
    dictionary.put("0", 0);
    dictionary.put("1", 1);
    dictionary.put("2", 2);
    dictionary.put("3", 3);
    dictionary.put("4", 4);
    dictionary.put("5", 5);
    dictionary.put("6", 6);
    dictionary.put("7", 7);
    dictionary.put("8", 8);
    dictionary.put("9", 9);
    dictionary.put("a", 10);
    dictionary.put("b", 11);
    dictionary.put("c", 12);
    dictionary.put("d", 13);
    dictionary.put("e", 14);
    dictionary.put("f", 15);
    dictionary.put("g", 16);
    dictionary.put("h", 17);
    dictionary.put("i", 18);
    dictionary.put("j", 19);
    dictionary.put("k", 20);
    dictionary.put("l", 21);
    dictionary.put("m", 22);
    dictionary.put("n", 23);
    dictionary.put("o", 24);
    dictionary.put("p", 25);
    dictionary.put("q", 26);
    dictionary.put("r", 27);
    dictionary.put("s", 28);
    dictionary.put("t", 29);
    dictionary.put("u", 30);
    dictionary.put("v", 31);
    dictionary.put("w", 32);
    dictionary.put("x", 33);
    dictionary.put("y", 34);
    dictionary.put("z", 35);
  }

  public static boolean isPrime(int num) {
    if (num <= 1) {
      return false;
    }
    for (int i = 2; i < num/2; i++) {
      if ((num % i) == 0) {
        return false;
      }
    }
    return true;
  }
  
  public static int prime(int num) { // returns the previous prime number smaller than num
    for (int i = num - 1; i > 1; i--) {
      if (isPrime(i)) {
        return i;
      }
    }
    return 1;
  }

  public static int hashfunc(String key, int database_length) { // converts key to initial index to be stored into database
    char[] characters = key.toCharArray();
    long total = 0;

    for (int i = 0; i < characters.length; i++) {
      total = total + dictionary.get(String.valueOf(characters[i]))
          * (long) Math.pow(dictionary.size(), characters.length - 1 - i);
    }

    return (int) (total % database_length);
  }

  public static boolean checkKey(String key) { // checks if key contains only alphanumerical characters
    for (int i = 0; i < key.length(); i++) {
      if (!dictionary.containsKey(Character.toString(key.charAt(i)))) {
        return true;
      }
    }
    return false;
  }

  public static int firstVacantIndex(DataItem[] database, int initial, int collision) { // finds the first available slot to insert
    int stepNumber = 1;
    int totalProbes = 0;
    int temp = initial;

    while (database[initial] != null) {
      if (collision == 1) {
        initial += stepNumber;
      }

      if (collision == 2) {
        if (totalProbes > database.length) { // if the amount of probes exceed the size of the database, it is an infinite loop
          return firstVacantIndex(database, (temp + 1) % database.length, collision); // restart probing at the next index
        }
        initial += (stepNumber * 2 - 1);
        stepNumber++;
        totalProbes++;
      }

      if (collision == 3) {
        stepNumber = prime(database.length) - temp % (prime(database.length));
        initial += stepNumber;
      }

      initial %= database.length;
    }

    return initial;
  }

  public static DataItem[] createdatabase(ArrayList<DataItem> datalist, int tablesize, int collision) {
    DataItem[] hashtable = new DataItem[tablesize];

    for (DataItem item : datalist) {
      insertdata(hashtable, item, collision);
    }

    return hashtable;
  }

  public static DataItem[] insertdata(DataItem[] database, DataItem data, int collision) {
    int index = hashfunc(data.getKey(), database.length);

    if (collision == 4) {
      DataItem temp = database[index];

      if (database[index] == null) {
        database[index] = data;
      } else {
        while (temp.getNext() != null) { // finds the DataItem which next is null
          temp = temp.getNext();
        }
        temp.setNext(data);
      }
    } else { // finds the first empty slot to insert data according to open addressing method
      database[firstVacantIndex(database, index, collision)] = data;
    }

    return database;
  }

  public static DataItem[] deletedata(DataItem[] database, String key, int collision) {
    DataItem data = searchdata(database, key, collision);

    if (data == null) {
      return database;
    }

    DataItem[] newdatabase = database.clone();
    if (collision == 4) {
      DataItem head = newdatabase[data.getIndex()];

      if (head.getNext() == null) { //if there is only one DataItem
        newdatabase[data.getIndex()] = null;
        return newdatabase;
      }
      if (head.getKey().equals(data.getKey())) { //if it is the first DataItem
        DataItem temp = head.getNext();
        newdatabase[data.getIndex()] = temp;
        return newdatabase;
      }
      while (!head.getNext().getKey().equals(data.getKey())) { //if it is elsewhere
        head = head.getNext();
      }
      DataItem after = head.getNext().getNext();
      head.setNext(after); // reconnect the DataItem chain after deletion

    } else { // for open addressing, just change the index to null
      newdatabase[data.getIndex()] = null;
    }
    return newdatabase;
  }

  public static DataItem searchdata(DataItem[] database, String key, int collision) {
    int index = hashfunc(key, database.length);
    DataItem temp = database[index];

    if (collision == 4) {
      if (database[index] == null) {
        return null;
      } else {
        while (!temp.getKey().equals(key)) {
          if (temp.getNext() == null) {
            return null;
          } else {
            temp = temp.getNext();
          }
        }
        temp.setIndex(index); // for easy access to its index
        return temp;
      }
    } else {
      int stepNumber = 1;
      int tempNumber = 1;
      int tempindex = index;
      int totalProbes = 0;
      Set<Integer> history = new HashSet<Integer>(); // used to check if the probing searched through every index

      if (database[index] == null) {
        return null;
      }

      while (!database[index].getKey().equals(key)) {
        if (collision == 1) {
          history.add(index);
          index += stepNumber;
        }

        if (collision == 2) {
          if (totalProbes > database.length) { // if the amount of probes exceed the size of the database, it is an infinite loop
            history.add(index);
            stepNumber = 1; // reset the stepNumber
            totalProbes = 0; // reset the totalProbes
            index = tempindex + tempNumber; // increment index by 1 after each restart of probing
            tempNumber++;
            index %= database.length;
            continue;
          }
          history.add(index);
          index += (stepNumber * 2 - 1);
          stepNumber++;
          totalProbes++;
        }

        if (collision == 3) {
          stepNumber = prime(database.length) - tempindex % (prime(database.length));
          history.add(index);
          index += stepNumber;
        }

        index %= database.length;

        if (database[index] == null) {
          return null;
        }

        if (history.size() == database.length) { // if checked every index, stop searching, it is possible for it to be last index
          break;
        }
      }

      if (!database[index].getKey().equals(key)) {
        return null;
      } else {
        database[index].setIndex(index); // for easy access to its index
        return database[index];
      }
    }
  }
  
  public static void printchain(DataItem item, int z) {
    System.out.printf("%d | %s | %s\n", z, item.getKey(), item.getDescription());
    if (item.getNext() != null) {
      printchain(item.getNext(), z);
    }
  }

  public static void main(String args[]) {

    Scanner mystring = new Scanner(System.in);
    Scanner myint = new Scanner(System.in);

    int tablesize = 0;
    while (true) {
      try {
        System.out.println("Welcome to our data storing program:");
        System.out.println("Input the memory size of the storage:");
        tablesize = myint.nextInt();
        int[] negativeerror = new int[tablesize];
        break;
      } catch (Exception e) {
        System.out.printf("You have gotten an input error: %s\n", e);
        System.out.println("Please try again.");
        myint.nextLine();
      }
    }

    int collision = 0;
    while (true) {
      try {
      System.out.println("\nWhich method would you like to be used to solve collision? (Input 1-4:)");
      System.out.println("1 - Linear Probing");
      System.out.println("2 - Quadratic Probing");
      System.out.println("3 - Double Hashing");
      System.out.println("4 - Separate Chaining");
      collision = myint.nextInt();
      }
      catch (Exception e) {
        System.out.printf("\nYou have gotten an input error: %s\n", e);
        System.out.println("Please try again.");
        myint.nextLine();
      }
      if (collision > 0 && collision < 5) {
        break;
      } else {
        System.out.println("\nYour input must be either 1,2,3 or 4. Please try again.");
      }
    }

    System.out.println("\nNow we will proceed to storing your data item. Each data item will have one key and one description.");
    System.out.println("You can only enter less than the memory you specified.");
    ArrayList<DataItem> datalist = new ArrayList<DataItem>();
    String key = "hi";
    String desc = "hi";
    int data_num = 0;
    int checker = 0;
    while (data_num < tablesize) {
      System.out.println("\nInput the data key (press enter to stop):");
      key = mystring.nextLine().toLowerCase();
      if (key.equals("")) {
        break;
      }
      if (key.length() > 12) {
        System.out.println("\nThe key is too long. Please enter a key with less than 13 characters.");
        continue;
      }
      if (checkKey(key)) {
        System.out.println("\nOnly alphanumeric characters are allowed.");
        continue;
      }
      checker = 0;
      while (true) {
        if (data_num != 0 && datalist.get(checker).getKey().equals(key)) {
          System.out.println("\nThis data contain the same key as previously stored data. Please enter a different key.");
          break;
        }
        checker++;
        if (checker >= data_num) {
          System.out.println("Input the data description:");
          desc = mystring.nextLine();
          datalist.add(new DataItem(key, desc));
          System.out.printf("\nData #%d has been inserted successfully.\n", data_num + 1);
          data_num++;
          break;
        }
      }
    }
    DataItem[] database = createdatabase(datalist, tablesize, collision);

    int action = 0;
    while (action != 5) {
      try {
        System.out.println("\nThe database is fully updated.");
        System.out.println("What would you like to do next?");
        System.out.println("1 - Insert a new data item");
        System.out.println("2 - Delete a data item");
        System.out.println("3 - Search for a data item");
        System.out.println("4 - Print the database");
        System.out.println("5 - End the program");
        action = myint.nextInt();
  
        if (action == 1) {
          if (data_num >= tablesize) {
            System.out.println("\nSorry, the memory is full. You must delete an item first before inserting a new one.");
            continue;
          } 
          while (true) {
            System.out.println("\nInput the data key:");
            key = mystring.nextLine().toLowerCase();
            if (checkKey(key)) {
              System.out.println("\nOnly alphanumeric characters are allowed.");
            } else if (key.length() > 12) {
              System.out.println("\nThe key is too long. Please enter a key with less than 13 characters.");
            } else if (searchdata(database, key, collision) != null) {
              System.out.println("\nSorry, your data contain the same key as one of the data in the database. Please enter a different key.");
            } else {
              break;
            }
          }
          System.out.println("Input the data description:");
          desc = mystring.nextLine();
          database = insertdata(database, new DataItem(key, desc), collision);
          data_num++;
        } else if (action == 2) {
          while (true) {
            System.out.println("\nInput the data key you wish to delete:");
            key = mystring.nextLine().toLowerCase();
            if (checkKey(key)) {
              System.out.println("\nOnly alphanumeric characters are allowed.");
            } else if (key.length() > 12) {
              System.out.println("\nThe key is too long. Please enter a key with less than 13 characters.");
            } else {
              DataItem[] olddatabase = deletedata(database, key, collision);
              if (database == olddatabase) {
                System.out.println("\nData item not found.");
                break;
              } else {
                database = olddatabase;
                System.out.println("\nData item deleted, database updated.");
                data_num--;
                break;
              }
            }
          }
        } else if (action == 3) {
          while (true) {
            System.out.println("\nSearch for the data item by its key:");
            key = mystring.nextLine().toLowerCase();
            if (checkKey(key)) {
              System.out.println("\nOnly alphanumeric characters are allowed.");
            } else if (key.length() > 12) {
              System.out.println("\nThe key is too long. Please enter a key with less than 13 characters.");
            } else {
              DataItem data = searchdata(database, key, collision);
              if (data == null) {
                System.out.println("\nData item not found.");
                break;
              } else {
                System.out.printf("\nData item found.\nKey: %s\nDesc: %s\n", data.getKey(), data.getDescription());
                break;
              }
            }
          }
        } else if (action == 4) {
          System.out.printf("\nDatabase Table with size %d\n", tablesize);
          System.out.println("----------------------------------");
          for (int z = 0; z < database.length; z++) {
            if (database[z] != null) {
              System.out.printf("%d | %s | %s\n", z, database[z].getKey(), database[z].getDescription());
              if (database[z].getNext() != null) {
                printchain(database[z].getNext(), z);
              }
            }
          }
        } else if (action != 5) {
          System.out.println("\nYour input must be either 1,2,3,4 or 5. Please try again.");
          }
        }
      catch (Exception e) {
        System.out.printf("\nYou have gotten an input error: %s\n", e);
        System.out.println("Please try again.");
        myint.nextLine();      
      }
    }
    System.out.println("\nProgram is ending...........");
  }
}