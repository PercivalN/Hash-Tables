class HashTableEntry:
    """
    Hash Table entry, as a linked list node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        
    

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """
    
    def __init__(self, capacity):
        self.capacity = capacity    # Sets the number of buckets in the hash table
        self.storage = [None] * capacity
        self.initial_capacity = capacity
        self.number_keys = 0

    def fnv1(self, key):
        """
        FNV-1 64-bit hash function
        
        For 64-bit:
            FNV_prime = 2^40 + 2^8 + 0xb3
            offset_basis = 14695981039346656037

        XOR operator ^

        hash = offset_basis
        for each octet_of_data to be hashed
            hash = hash * FNV_prime
            hash = hash xor octet_of_data
        return hash

        Implement this, and/or DJB2.
        """
        
        FNV_prime = 2**40 + 2**8 + 0xb3
        hash = 14695981039346656037
        for x in key:
            hash = hash * FNV_prime
            hash = hash ^ ord(x)
        return hash & 0xFFFFFFFFFFFFFFFF
        
    def djb2(self, key):
        """
        DJB2 32-bit hash function

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF

    def _hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity
    
    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        #self.size_check()
        hashed_key = self._hash_index(key)
        new_linked_pair = HashTableEntry(key, value)

        node = self.storage[hashed_key]
        if node is None:
            self.storage[hashed_key] = new_linked_pair
            self.number_keys += 1
            return

        while node is not None and node.key != key:
            prev = node
            node = node.next

        if node is None:
            prev.next = new_linked_pair
            self.num_keys += 1

        else:
            # The key was found, so update the value
            node.value = value
       
    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Get the hashed_key.
        hashed_key = self._hash_index(key)

        # Get the value stored in storage at that hashed_key.
        node = self.storage[hashed_key]

        # If that node is the desired one, point the storage[hashed_key] to its next.
        if node.key == key:
            self.storage[hashed_key] = node.next
            self.number_keys -= 1
            #self.size_check()
            return

        # Traverse the LL until the key is found or the end of the LL is reached.

        while node is not None and node.key != key:
            prev = node
            node = node.next

        if node is None:
            print(f'{key} was not found')
            return None
        # Remove the LinkedPair node from the chain by assigning
        # the .next pointer of the previous node to be the node that its .next pointer was pointing to.
        prev.next = node.next
        self.num_keys -= 1
        self.size_check()
        
    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Compute hash
        hashed_key = self._hash_index(key)

        # Get the first node in LL in storage
        node = self.storage[hashed_key]

        # Traverse the linked list at this node until the key is found or the end is reached
        while node is not None and node.key != key:
            node = node.next

        if node is None:
            return None
        else:
            return node.value

    def resize(self):
        """
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Implement this.
        """
       
        

if __name__ == "__main__":
    ht = HashTable(2)

    ht.put("line_1", "Tiny hash table")
    ht.put("line_2", "Filled beyond capacity")
    ht.put("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")
