#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAPACITY 50000 // Size of the HashTable.

typedef struct Ht_item
{
    char *key;
    char *value;
} Ht_item;

// Required to use inside the struct
// Forward struct declaration
typedef struct LinkedList LinkedList;

typedef struct LinkedList
{
    Ht_item *item;
    LinkedList *next;
} LinkedList;

typedef struct HashTable
{
    // Contains an array of pointers to items.
    Ht_item **items;
    LinkedList **overflow_buckets;
    int size;
    int count;
} HashTable;

unsigned long hash_function(char *str);
LinkedList *allocate_list();
LinkedList *linkedlist_insert(LinkedList *list, Ht_item *item);
Ht_item *linkedlist_remove(LinkedList *list);
void free_linkedlist(LinkedList *list);
LinkedList **create_overflow_buckets(HashTable *table);
void free_overflow_buckets(HashTable *table);
Ht_item *create_item(char *key, char *value);
HashTable *create_table(int size);
void free_item(Ht_item *item);
void free_table(HashTable *table);
void handle_collision(HashTable *table, unsigned long index, Ht_item *item);
void ht_insert(HashTable *table, char *key, char *value);
char *ht_search(HashTable *table, char *key);
void ht_delete(HashTable *table, char *key);
void print_search(HashTable *table, char *key);
void print_table(HashTable *table);

/* 
    Driver Coder
    
int main()
{
    HashTable *ht = create_table(CAPACITY);
    ht_insert(ht, (char *)"1", (char *)"First address");
    ht_insert(ht, (char *)"2", (char *)"Second address");
    ht_insert(ht, (char *)"Hel", (char *)"Third address");
    ht_insert(ht, (char *)"Cau", (char *)"Fourth address");
    print_search(ht, (char *)"1");
    print_search(ht, (char *)"2");
    print_search(ht, (char *)"3");
    print_search(ht, (char *)"Hel");
    print_search(ht, (char *)"Cau"); // Collision!
    print_table(ht);
    ht_delete(ht, (char *)"1");
    ht_delete(ht, (char *)"Cau");
    print_table(ht);
    free_table(ht);
    return 0;
}
*/

/*
    Used in Python
    1. create_table -> hidden... inherited from dictionary
    2. ht_insert
    3. print_search
    4. ht_delete
    5. free_table -> hidden
*/
