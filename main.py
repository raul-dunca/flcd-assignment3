

class Node:
    def __init__(self, val):
        self.value=val
        self.next= None

    def __str__(self):
        return str(self.value)

class MyHashTable:
    def __init__(self, cap):
        self.capacity=cap
        self.list=[None] * (self.capacity)
        #self.size=0

    def hash_fct(self,obj):
        return hash(obj) % self.capacity

    def lookup(self,obj):
        idx = self.hash_fct(obj)
        if self.list[idx] is None:
            return False
        else:
            current=self.list[idx]
            while current.next is not None:
                if current.value==obj:
                    return True
                current = current.next
            if current.value==obj:
                return True
            return False

    def add(self, obj):
        idx=self.hash_fct(obj)
        if self.list[idx] is None:
            self.list[idx]=Node(obj)
        else:
            current=self.list[idx]
            while current.next is not None:
                if current.value==obj:
                    return
                current=current.next
            if current.value == obj:
                return
            current.next=Node(obj)

    def __str__(self):
        output=""
        for i in self.list:
            output += "List "
            if i is not None:
                while i.next is not None:
                    output+= str(i) + ' '
                    i = i.next
            output+= str(i) + '\n'
        return output


m=MyHashTable(10)
n=MyHashTable(50)
m.add("a")
m.add("a")
m.add("b")
m.add("c")
m.add("d")

for i in range(100):
    n.add(i)

print("Identifiers ST")
print("Is a in m: "+str(m.lookup("a")))
print("Is 2 in m: "+str(m.lookup(2)))
print("Constants ST")
print("Is c in n: "+str(n.lookup("c")))
print("Is 95 in n: "+str(n.lookup(95)))
print("Is 102 in n: "+str(n.lookup(102)))



identifiers_sym_tbl = MyHashTable(10)
consts_sym_tbl = MyHashTable(20)
PIF = []

tokens=[]
separators=[]
operators=[]
with open("token.in", 'r') as file:
    for line in file:
        tokens.append(line.replace('\n',''))


separators=tokens[17:27]
separators.append('\n')
separators.append('\t')

operators=tokens[2:17]
print("\n")
file_path = input("Enter the file name (e.g., a.txt):")

error=False
glb_error=False
line_cntr=0
with open(file_path, 'r') as file:
    for line in file:
        line_cntr+=1
        token=""
        ok=True
        error=False
        for i in line:
            if i=='"':
                if ok==False:       # we found the closing "
                    token+='"'
                    consts_sym_tbl.add(token)
                    PIF.append(("const",consts_sym_tbl.hash_fct(token)))
                    #print(token+" is a string const!")
                    token=""
                ok=not ok
            if ok==False:
                token+=i
                continue
            if i in separators or i in operators:
                if token not in tokens and token !="":
                    if token.isnumeric():
                        consts_sym_tbl.add(token)
                        PIF.append(("const", consts_sym_tbl.hash_fct(token)))
                        if i !=' ' and i!='\n' and i!='\t':
                            PIF.append((i, -1))
                        #print(token+ " is a int const!")
                    elif token[0].isalpha():
                        for j in range (1,len(token)):
                            if not token[j].isdigit() and not token[j].isalpha() and token[j]!='_':
                                print(token + " is not a valid identifier! On line: "+str(line_cntr))
                                error=True
                                glb_error=True
                        if error==False:
                            identifiers_sym_tbl.add(token)
                            PIF.append(("id", identifiers_sym_tbl.hash_fct(token)))
                            if i != ' ' and i != '\n' and i != '\t':
                                PIF.append((i, -1))
                            #print(token + " is a identifier!")
                    else:
                        print(token + " is  undefined; On line: " + str(line_cntr))
                        #error=True
                        glb_error = True
                else:
                    if token !="":
                        PIF.append((token, -1))
                    if i != ' ' and i != '\n' and i != '\t' and i!='"':
                        PIF.append((i, -1))
                token = ""
            else:
                token+=i

        if ok==False:
            print("You forgot to close the \" on line " +str(line_cntr))
            glb_error=True


    if not glb_error:
        print("Program is lexically correct!")
        with open('ST.out', 'w') as file:
            file.write("The data structure used for the ST is hashmap.\n\n")
            file.write("Identifier Symbol Table.\n")
            file.write(str(identifiers_sym_tbl))
            file.write("\n")
            file.write("Constants Symbol Table.\n")
            file.write(str(consts_sym_tbl))

        with open('PIF.out', 'w') as file:
            for pair in PIF:
                file.write(str(pair)+ "\n")

    else:
        with open('ST.out', 'w'):
            pass
        with open('PIF.out', 'w'):
            pass