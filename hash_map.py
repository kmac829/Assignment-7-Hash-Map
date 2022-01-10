# Name: Katie Schaumleffle
# OSU Email: schaumlk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/2021
# Description: Implement a hashmap including the following methods: put(), get(), remove()
#               contains_key(), clear(), empty_buckets(), resize_table(), table_load()
#               and get_keys()


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the contents of the hashmap. Does not change the hash table
        capacity.
        """
        #loop through clearing buckets
        for i in range(self.buckets.length()):
            self.buckets.set_at_index(i, LinkedList())
        #once cleared, reset size to 0
        self.size = 0    
    

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key.
        """
        hash_val = self.hash_function(key)
        index = hash_val % self.capacity
        list = self.buckets.get_at_index(index)

        #return if empty or if key is not in the hashmap
        if self.buckets.length() == 0 or list.contains(key) is None:
            return None

        #If we get here, it's not empty and is in the hashmap- return the value
        else:
            return list.contains(key).value

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pairs in the hashmap. If a given key already exists,
        it's associated value is replaced with the new value. If a key is not in the hashmap, 
        a key/value pair is added.
        """
        hash_val = self.hash_function(key) 
        index = hash_val % self.capacity
        list = self.buckets.get_at_index(index)

        #If key is not in hashmap, add key/value pair
        if list.contains(key) is None:
            list.insert(key, value)
            self.size += 1
        #If key exists, replace with new value
        else:
            list.remove(key)
            list.insert(key, value)
        
    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hashmap.
        """
        hash_val = self.hash_function(key)
        index = hash_val % self.capacity
        list = self.buckets.get_at_index(index)

        # if hash map contains the key: find node and remove it
        if self.contains_key(key):
            list.remove(key)
            #readjust size
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        This method returns True is the given key is in the hashmap, otherwise returns false.
        """
        hash_val = self.hash_function(key)
        index = hash_val % self.capacity
        list = self.buckets.get_at_index(index) 

        #If the key is in the hashmap, return true
        if list.contains(key):
            return True
        #If we get here, value is not in hashmap and we can return false
        else:
            return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hashtable.
        """
        count = 0
        #loop through hashmap
        for i in range(self.buckets.length()):
            #if a bucket is empty, increase count variable by one
            if self.buckets.get_at_index(i).length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """
        return self.size/ self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. Existing key/value pairs
        must remain in the new hash map and all hash table links must be rehashed.
        """
        #This method does nothing if new_capacity is less than 1
        if new_capacity < 1:
            return
        
        #create empty dynamic array for updated buckets 
        new_array = DynamicArray()
        for i in range(new_capacity):
            #copy list to new array
            new_array.append(LinkedList())

        #get current linked list
        for i in range(self.buckets.length()):
            current_list = self.buckets.get_at_index(i)
            #as long as there as buckets, loop through to update bucket locations
            if current_list.length() >= 0:
                for node in current_list:
                    hash_val = self.hash_function(node.key)
                    new_array_index = hash_val % new_capacity
                    #insert new buckets into array
                    new_array.get_at_index(new_array_index).insert(node.key, node.value)
        
        #update buckets and capacity
        self.buckets = new_array
        self.capacity = new_capacity
        
    def get_keys(self) -> DynamicArray:
        """
        This method returns a da that contains all keys stored in the hashmap
        """
        new_array = DynamicArray()

        #loop through buckets copying to new array
        for i in range(self.buckets.length()):
            for node in self.buckets.get_at_index(i):
                new_array.append(node.key)

        return new_array


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
