memory = []

BIT = 64

BYTE = 1
WORD = 2
QWORD = 4
DWORD = 8

class ptr: ...
def byte(): ...
def word(): ...
def qword(): ...
def dword(): ...

class ptr:
    def __init__(self, addr: int, bytes: int = BYTE, big_endian: bool = False): 
        self.addr = addr
        self.bytes = bytes
        self.big_endian = big_endian

    def __add__(self, val: int):
        return ptr(self.addr + val, self.bytes, self.big_endian)

    def __getitem__ (self, idx):
        if type(idx) == slice:
            res = []
            s = idx.indices(2 ** BIT)
            for i in range(s[0],s[1],s[2]):
                res.append(self[i])
            return res

        if type(idx) == int:
            global memory
            while self.addr + (idx * self.bytes) + self.bytes > len(memory): memory += [0]
            res = 0
            elements = [memory[self.addr + (self.bytes * idx) + i] for i in range(self.bytes)]
            if self.big_endian == True:
                elements.reverse()
            while len(elements) > 0:
                res *= 0x100
                res += elements[-1]
                elements = elements[:-1]
            return res
        
        raise TypeError("ptr indices must be integers or slices, not " + type(idx).__name__)

    def __setitem__(self, idx, value):
        if type(idx) == int:
            if type(value) == int:
                res = []
                for i in range(self.bytes):
                    res.append(value % 0x100)
                    value //= 0x100
                if self.big_endian == True:
                    res.reverse()

                global memory
                while self.addr + (idx * self.bytes) + self.bytes > len(memory): memory += [0]
                for i in range(self.bytes):
                    memory[self.addr + (self.bytes * idx) + i] = (res[i]) & 0xff
                    
                return self

            for i in range(len(value)):
                self.__setitem__(idx + i, value[i])
            return self
        
        raise TypeError("unhashable type: 'slice'")

    def showMemory(self, count):
        print(".",end=' ')
        for i in range(0xff):
            print(hex(i)[2:],end=' ')
        print()
        for i in range(count // 16 + 1):
            pass
            

def byte(pointer):
    return ptr(pointer.addr,1,pointer.big_endian)

def word(pointer):
    return ptr(pointer.addr,2,pointer.big_endian)
    
def qword(pointer):
    return ptr(pointer.addr,4,pointer.big_endian)
    
def dword(pointer):
    return ptr(pointer.addr,8,pointer.big_endian)
