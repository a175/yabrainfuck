import sys

class InfiniteTape:
    def __init__(self,default_value = 0):
        self.default_value = default_value
        self.reset_values()
        
    def move_header_right(self):
        if [] == self.tape_r:
            self.tape_r.append(self.default_value)
        self.tape_l.append(self.data_at_header)
        self.data_at_header=self.tape_r.pop()

    def move_header_left(self):
        if [] == self.tape_l:
            self.tape_l.append(self.default_value)
        self.tape_r.append(self.data_at_header)
        self.data_at_header=self.tape_l.pop()

    def get_value(self):
        return self.data_at_header
    
    def increase_value(self):
        self.data_at_header+=1
        
    def decrease_value(self):
        self.data_at_header-=1
        
    def set_value(self,v):
        self.data_at_header=v
        
    def reset_values(self):
        self.tape_l = []
        self.data_at_header = self.default_value
        self.tape_r = []


class CodeTape(InfiniteTape):
    def __init__(self,default_value = 0):
        super().__init__(default_value=None)
        

class BrainFuckVM:
    CODE_PI=0
    CODE_PD=2
    CODE_VI=3
    CODE_VD=5
    CODE_SO=6
    CODE_SI=4
    CODE_BO=7
    CODE_BC=1
    CODE_TABLE=[('<', CODE_PI), ('>', CODE_PD), ('+', CODE_VI), ('-', CODE_VD), ('.', CODE_SO), (',', CODE_SI), ('[', CODE_BO), (']', CODE_BC)]
    
    def __init__(self,output=sys.stdout,input=sys.stdin):
        self.tape=InfiniteTape()
        self.code=CodeTape()
        self.flag=0
        self.output=output
        self.input=input
        
    def set_codelist(self,code_list):
        self.code.reset_values()
        for i in reversed(code_list):
            self.code.move_header_left()
            self.code.set_value(i)
        
    def run(self):
        self.flag=0
        while(self.code.get_value() != None):
            self.exec_a_code()

    def exec_a_code(self):
        code = self.code.get_value()
        if code == self.CODE_PI:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_PI()
        elif code == self.CODE_PD:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_PD()
        elif code ==  self.CODE_VI:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_VI()
        elif  code ==  self.CODE_VD:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_VD()
        elif code ==  self.CODE_SO:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_SO()
        elif code ==  self.CODE_SI:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_CODE_SI()
        elif code ==  self.CODE_BO:
            if self.flag > 0:
                self.flag += 1
                self.do_SKIP_F()
            elif self.flag < 0:
                self.flag += 1
                if self.flag < 0:
                    self.do_SKIP_B()
            else:
                v = self.tape.get_value()
                if v == 0:
                    self.flag=1
                    self.do_CODE_BO_SKIP()
                else:
                    self.do_CODE_BO_DO()
                
        elif code == self.CODE_BC:
            if self.flag > 0:
                self.flag -= 1
                self.do_SKIP_F()
            elif self.flag < 0:
                self.flag -= 1
                self.do_SKIP_B()
            else:
                v = self.tape.get_value()
                if v != 0:
                    self.flag = -1
                    self.do_CODE_BC_SKIP()
                else:
                    self.do_CODE_BC_DO()
        else:
            if self.flag > 0:
                self.do_SKIP_F()
            elif self.flag < 0:
                self.do_SKIP_B()
            else:
                self.do_OTHER_CODE()
            
    def do_SKIP_F(self):
        self.code.move_header_right()
    
    def do_SKIP_B(self):
        self.code.move_header_left()
        
    def do_CODE_PI(self):
        self.tape.move_header_right()
        self.code.move_header_right()

    def do_CODE_PD(self):
        self.tape.move_header_left()
        self.code.move_header_right()

    def do_CODE_VI(self):
        self.tape.increase_value()
        self.code.move_header_right()

    def do_CODE_VD(self):
        self.tape.decrease_value()
        self.code.move_header_right()
        
    def do_CODE_SO(self):
        r=self.tape.get_value()
        self.output.write(chr(r))
        self.code.move_header_right()
        
    def do_CODE_SI(self):
        c=self.input.read(1)
        self.tape.set_value(c)
        self.code.move_header_right()

    def do_CODE_BO_SKIP(self):
        self.code.move_header_right()
        
    def do_CODE_BO_DO(self):
        self.code.move_header_right()
    
    def do_CODE_BC_SKIP(self):
        self.code.move_header_left()
        
    def do_CODE_BC_DO(self):
        self.code.move_header_right()
    
    def do_OTHER_CODE(self):
        pass
    
class BrainFuckCompilier:    
    def __init__(self,target_brainfuckvm):
        self.code_table={}
        for (s,c) in target_brainfuckvm.CODE_TABLE:
            self.code_table[self.get_code_for_a_token(s)]=c
        self.CODE_BO=target_brainfuckvm.CODE_BO
        self.CODE_BC=target_brainfuckvm.CODE_BC
        self.default_takens=['.',',','[',']','+','-','<','>']

    def get_codelist_from_text(self, codetext):
        r = []
        for ti in self.xtokens_from_text(codetext):
            r.append(self.code_table[self.get_code_for_a_token(ti)])
        return r

    def xtokens_from_text(self, codetext):
        for ti in codetext:
            yield ti

    def get_code_for_a_token(self,t):
        n=ord(t)
        return (5*n+4*(n // 16)+3*(n//16//16)+2*(n//16//16//16)+(n//16//16//16//16))%8


    def get_equivalent_token(self,code,shift,candidate):
        shift = shift % len(candidate)
        for cand in candidate[shift:]+candidate:
            if code == self.get_code_for_a_token(cand):
                return cand
        for cand in self.default_tokens:
            if code == self.get_code_for_a_token(cand):
                return cand

    def get_equivalent_code_text(self,code_list,candidates,shift_weight):
        ans=""
        for shift,code in enumerate(code_list):
            ans=ans+self.get_equivalent_token(code,shift*shift_weight,candidates)
        return ans
        
if __name__ == '__main__':
    bfvm=BrainFuckVM()
    bfc = BrainFuckCompilier(bfvm)
    codetorun = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    codelist = bfc.get_codelist_from_text(codetorun)
    bfvm.set_codelist(codelist)
    bfvm.run()

