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


class VirtualMachine:
    CODE_PI=0
    CODE_PD=2
    CODE_VI=3
    CODE_VD=5
    CODE_SO=6
    CODE_SI=4
    CODE_BO=7
    CODE_BC=1
    CODE_TABLE=[('>', CODE_PI), ('<', CODE_PD), ('+', CODE_VI), ('-', CODE_VD), ('.', CODE_SO), (',', CODE_SI), ('[', CODE_BO), (']', CODE_BC)]

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

class BrainFuckCompileError(Exception):
    def __init__(self,name):
        self.name = name

class Complier:
    def __init__(self,target_brainfuckvm):
        self.CODE_BO=target_brainfuckvm.CODE_BO
        self.CODE_BC=target_brainfuckvm.CODE_BC
        self.CODE_PI=target_brainfuckvm.CODE_PI
        self.CODE_PD=target_brainfuckvm.CODE_PD
        self.CODE_VI=target_brainfuckvm.CODE_VI
        self.CODE_VD=target_brainfuckvm.CODE_VD
        self.CODE_SO=target_brainfuckvm.CODE_SO
        self.CODE_SI=target_brainfuckvm.CODE_SI
        self.default_tokentext=['.',',','[',']','+','-','<','>']

    def get_codelist_from_text(self, codetext):
        r = []
        stack = 0
        for ci in self.xcode_from_text(codetext):
            if ci == self.CODE_BO:
                stack = stack+1
            if ci == self.CODE_BC:
                stack = stack-1
                if stack < 0:
                    raise BrainFuckCompileError("unpaired ]")
            r.append(ci)
        if stack > 0:
            raise BrainFuckCompileError("unpaired [")
        return r

    def get_modulo_ord(self,c):
        n=ord(c)
        return (5*n+4*(n // 16)+3*(n//16//16)+2*(n//16//16//16)+(n//16//16//16//16))%8

    def get_code_for_tokentext(self, c):
        t=self.get_modulo_ord(c)
        code_table=[('<', self.CODE_PI), ('>', self.CODE_PD), ('+', self.CODE_VI), ('-', self.CODE_VD), ('.', self.CODE_SO), (',', self.CODE_SI), ('[', self.CODE_BO), (']', self.CODE_BC)]
        for (s,c) in code_table:
            if self.get_modulo_ord(s)==t:
                return c

    def xcode_from_text(self, codetext):
        for ti in codetext:
            yield self.get_code_for_tokentext(ti)


    def get_equivalent_tokentext(self,code,shift,candidate):
        shift = shift % len(candidate)
        for cand in candidate[shift:]+candidate:
            if code == self.get_code_for_tokentext(cand):
                return cand
        for cand in self.default_tokentext:
            if code == self.get_code_for_tokentext(cand):
                return cand

    def get_equivalent_code_text(self,code_list,candidates,shift_weight):
        ans=""
        for shift,code in enumerate(code_list):
            ans=ans+self.get_equivalent_tokentext(code,shift*shift_weight,candidates)
        return ans

class SimpleComplier:
    def __init__(self,target_brainfuckvm,error_if_unknown_char=False):
        self.CODE_BO=target_brainfuckvm.CODE_BO
        self.CODE_BC=target_brainfuckvm.CODE_BC
        self.CODE_PI=target_brainfuckvm.CODE_PI
        self.CODE_PD=target_brainfuckvm.CODE_PD
        self.CODE_VI=target_brainfuckvm.CODE_VI
        self.CODE_VD=target_brainfuckvm.CODE_VD
        self.CODE_SO=target_brainfuckvm.CODE_SO
        self.CODE_SI=target_brainfuckvm.CODE_SI
        self.token_table=[]
        self.setup_token_table()
        self.error_if_unknown_char=error_if_unknown_char

    def setup_token_table(self):
        pass
        
    def add_to_token_table(self,code,tokentext):
        self.token_table.append((code,tokentext))
    
    def get_codelist_from_text(self, codetext):
        r = []
        stack = 0
        for ci in self.xcode_from_text(codetext):
            if ci == self.CODE_BO:
                stack = stack+1
            if ci == self.CODE_BC:
                stack = stack-1
                if stack < 0:
                    raise BrainFuckCompileError("unpaired ]")
            r.append(ci)
        if stack > 0:
            raise BrainFuckCompileError("unpaired [")
        return r


    def xcode_from_text(self, codetext):
        while len(codetext)>0:
            for (code,t) in self.token_table:
                if codetext.startswith(t):
                    yield code
                    codetext=codetext[len(t):]
                    break
            else:
                if self.error_if_unknown_char:
                    raise BrainFuckCompileError("unknown token")
                codetext=codetext[1:]


    def get_equivalent_tokentext(self,code,shift):
        shift = shift % len(self.token_table)
        for cand in self.token_table[shift:]+self.token_table:
            if code == self.get_code_for_tokentext(cand):
                return cand
        raise BrainFuckCompileError("NotFoundCorrespondingToken Error")

    def get_equivalent_code_text(self,code_list,shift_weight):
        ans=""
        for shift,code in enumerate(code_list):
            ans=ans+self.get_equivalent_tokentext(code,shift*shift_weight)
        return ans

class StrictBFComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,">"),
            (self.CODE_PD,"<"),
            (self.CODE_VI,"+"),
            (self.CODE_VD,"-"),
            (self.CODE_SI,","),
            (self.CODE_SO,"."),
            (self.CODE_BO,"["),
            (self.CODE_BC,"]")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)
    
class NyarukoComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,"(」・ω・)」うー(／・ω・)／にゃー"),
            (self.CODE_PD,"(」・ω・)」うー!!(／・ω・)／にゃー!!"),
            (self.CODE_VI,"(」・ω・)」うー!(／・ω・)／にゃー!"),
            (self.CODE_VD,"(」・ω・)」うー!!!(／・ω・)／にゃー!!!"),
            (self.CODE_SI,"cosmic!"),
            (self.CODE_SO,"Let's＼(・ω・)／にゃー"),
            (self.CODE_BO,"CHAOS☆CHAOS!"),
            (self.CODE_BC,"I WANNA CHAOS!")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

class KemonoComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,"たのしー！"),
            (self.CODE_PD,"すごーい！"),
            (self.CODE_VI,"たーのしー！"),
            (self.CODE_VD,"すっごーい！"),
            (self.CODE_SI,"おもしろーい！"),
            (self.CODE_SO,"なにこれなにこれ！"),
            (self.CODE_BO,"うわー！"),
            (self.CODE_BC,"わーい！")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

class OokComplier(SimpleComplier):
    def __init__(self,target_brainfuckvm):
        super().__init__(target_brainfuckvm,error_if_unknown_char=True)
        
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,"Ook. Ook? "),
            (self.CODE_PD,"Ook? Ook. "),
            (self.CODE_VI,"Ook. Ook. "),
            (self.CODE_VD,"Ook! Ook! "),
            (self.CODE_SI,"Ook. Ook! "),
            (self.CODE_SO,"Ook! Ook. "),
            (self.CODE_BO,"Ook! Ook? "),
            (self.CODE_BC,"Ook? Ook! ")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

class BFBASICnComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,"す"),
            (self.CODE_PD,"ばぼーん"),
            (self.CODE_VI,"ぽ"),
            (self.CODE_VD,"び"),
            (self.CODE_SI,"うすらの"),
            (self.CODE_SO,"ぽーん"),
            (self.CODE_BO,"すてらの"),
            (self.CODE_BC,"なばびこーん")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

class MisaComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,">"),
            (self.CODE_PI,"→"),
            (self.CODE_PI,"～"),
            (self.CODE_PI,"ー"),
            (self.CODE_PD,"<"),
            (self.CODE_PD,"←"),
            (self.CODE_PD,"★"),
            (self.CODE_PD,"☆"),
            (self.CODE_VI,"+"),
            (self.CODE_VI,"あ"),
            (self.CODE_VI,"ぁ"),
            (self.CODE_VI,"お"),
            (self.CODE_VI,"ぉ"),
            (self.CODE_VD,"-"),
            (self.CODE_VD,"っ"),
            (self.CODE_VD,"ッ"),
            (self.CODE_SI,","),
            (self.CODE_SI,"？"),
            (self.CODE_SO,"."),
            (self.CODE_SO,"！"),
            (self.CODE_BO,"["),
            (self.CODE_BO,"「"),
            (self.CODE_BO,"『"),
            (self.CODE_BC,"]"),
            (self.CODE_BC,"」"),
            (self.CODE_BC,"』")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

class VariantComplier(SimpleComplier):
    def setup_token_table(self):
        tokenlist=[
            (self.CODE_PI,""),
            (self.CODE_PD,""),
            (self.CODE_VI,""),
            (self.CODE_VD,""),
            (self.CODE_SI,""),
            (self.CODE_SO,""),
            (self.CODE_BO,""),
            (self.CODE_BC,"")
        ]
        for (c,t) in tokenlist:
            self.add_to_token_table(c,t)

if __name__ == '__main__':
    bfvm=VirtualMachine()
    bfc = Complier(bfvm)
    codetorun = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    codelist = bfc.get_codelist_from_text(codetorun)
    bfvm.set_codelist(codelist)
    bfvm.run()


