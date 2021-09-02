# -*- encoding=utf8 -*-
__author__ = "qing"

from airtest.core.api import *

auto_setup(__file__)

mapper = {
    'masterSkill_xy': [(0.71, 0.43), (0.78, 0.43), (0.85, 0.43)],
    'change_xy_team': [(0.1, 0.5), (0.27, 0.5), (0.43, 0.5)],
    'change_xy_support': [(0.56, 0.5), (0.73, 0.5), (0.88, 0.5)],
    'yes': Template(r"tpl1628582592565.png", record_pos=(0.147, 0.159), resolution=(1334, 750)),
    'continueSummon': Template(r"tpl1630478038356.png", record_pos=(0.095, 0.239), resolution=(1334, 750)),
    'qp_15': Template(r"tpl1628524537457.png", record_pos=(-0.369, 0.004), resolution=(1334, 750)),
    'exp': Template(r"tpl1628494829189.png", record_pos=(0.139, 0.082), resolution=(1334, 750)),
    'qp' : Template(r"tpl1628484048479.png", record_pos=(0.22, -0.175), resolution=(1334, 750)),
    'caber_text' : Template(r"tpl1628484084333.png", record_pos=(-0.165, -0.057), resolution=(1334, 750)),
    'beginButton_pic' : Template(r"tpl1628484133012.png", record_pos=(0.43, 0.243), resolution=(1334, 750)),
    'masterSkill_pic' : Template(r"tpl1628484176489.png", record_pos=(0.434, -0.036), resolution=(1334, 750)),
    'battleMenu_pic' : Template(r"tpl1628484208799.png", record_pos=(0.435, -0.118), resolution=(1334, 750)),
    'servantSkills_x': [
        [0.06, 0.13, 0.2],
        [0.3, 0.37, 0.45],
        [0.55, 0.63, 0.7]
    ],
    'servantSkills_y': 0.8,
    'chooseTarget_text': Template(r"tpl1628484595661.png", record_pos=(0.004, -0.132), resolution=(1334, 750)) ,
    'allyTarget_x': [0.25, 0.5, 0.75],
    'allyTarget_y': 0.6,
    'attack_pic': Template(r"tpl1628484755150.png", record_pos=(0.396, 0.194), resolution=(1334, 750)),
    'noble_x': [0.3, 0.5, 0.7],
    'noble_y': 0.3,
    'cmd_x' : [0.1, 0.3, 0.5, 0.7, 0.9],
    'cmd_y' : 0.7,
    'return_pic': Template(r"tpl1628485036869.png", record_pos=(0.436, 0.249), resolution=(1334, 750)),
    'battleFinish': Template(r"tpl1628485458311.png", record_pos=(0.0, 0.22), resolution=(1334, 750)),
    'next_pic': Template(r"tpl1628485561564.png", record_pos=(0.372, 0.247), resolution=(1334, 750)),
    'close': Template(r"tpl1628485592234.png", record_pos=(-0.148, 0.158), resolution=(1334, 750)),
#     'continue': Template(r"tpl1628485616130.png", record_pos=(0.154, 0.162), resolution=(1334, 750)),
    'continue': (0.67, 0.78),
    'x': Template(r"tpl1630081753904.png", record_pos=(0.46, -0.179), resolution=(1334, 750)),
    'change': Template(r"tpl1630081858522.png", record_pos=(0.014, 0.207), resolution=(1334, 750)),
}


def waitActionDone(signal='masterSkill_pic', timeout=20, interval=0.5):
    '''
    等待施法动画\n
    默认等待御主技能出现
    '''
    sleep(interval)
    wait(mapper[signal], timeout=timeout)
    sleep(0.5)


def servantSkill(servant_idx, skill_idx, target=None):
    '''
    施法从者技能 \n
    从者idx [1, 2, 3] \n
    技能idx [1, 2, 3] \n
    等待施法完毕
    '''
    options = [1, 2, 3]
    if servant_idx not in options or skill_idx not in options:
        raise ValueError(f'Invalid input servant id: {servant_idx} or skill id {skill_idx}') 
    touch([mapper['servantSkills_x'][servant_idx-1][skill_idx-1], mapper['servantSkills_y']])
    if target:
        wait(mapper['chooseTarget_text'])
        touch([mapper['allyTarget_x'][target-1], mapper['allyTarget_y']])
        
    waitActionDone()

def masterSkill(skill_idx, ifChange=False, target=None):
    '''
    衣服技能 \n
    技能idx [1, 2, 3] \n
    目标(如果有) [1, 2, 3]
    '''
    touch(mapper['masterSkill_pic'])
    sleep(0.3)
    touch(mapper['masterSkill_xy'][skill_idx-1])
    if target is not None:
        waitActionDone('x')
        if ifChange:
            touch(mapper['change_xy_team'][target[0]-1])
            sleep(0.1)
            touch(mapper['change_xy_support'][target[1]-1])
            touch(mapper['change'])
    waitActionDone()

# masterSkill(3, ifChange=True, target=(3, 1))

def orderChange(target):
    masterSkill(3, ifChange=True, target=target)

def normalCmd(position, sleepTime=0.1):
    '''
    普通指令卡\n
    position [1, 2, 3, 4, 5]
    '''
    options = [1, 2, 3, 4, 5]
    if position not in options:
        raise ValueError(f'Invalid poistion: {position}')
    touch([mapper['cmd_x'][position-1], mapper['cmd_y']])
    sleep(sleepTime)


def nobleCmd(servant_idx=None, sleepTime=0.1):
    '''
    宝具\n
    从者idx [1, 2, 3]
    '''
    touch([mapper['noble_x'][servant_idx-1 if servant_idx is not None else 1], mapper['noble_y']])
    sleep(sleepTime)

    
def attack(noble_idx=None, ifwait=True):
    touch(mapper['attack_pic'])
    waitActionDone('return_pic')
    nobleCmd(servant_idx=noble_idx)
    normalCmd(1)
    normalCmd(2)
    if ifwait:
        waitActionDone('attack_pic', timeout=60, interval=0.5)
    
    
def battleFinish():
    for _ in range(2):
        touch(wait(mapper['battleFinish']))
        sleep(0.2)
    touch(wait(mapper['next_pic']))


def chooseFriend():
    # TODO
    touch(mapper['caber_text'])

def beginBattle():
    touch(mapper['beginButton_pic'])
    wait(mapper['attack_pic'])

def qpGateBattle():
    touch(mapper['qp_gate_text'])
    chooseFriend()
    beginBattle()
    skills = {
        1: (1, (2, 2), (3, 2)),
        2: (2, ),
        3: (1, (2, 2),  (3, 2))
    }
    castSkills(skills)
    attack()
    waitActionDone(timeout=40)
    attack()
    waitActionDone(timeout=40)
    attack()
    waitActionDone(signal='battleFinish', timeout=40)
    battleFinish()
    done()
      

def enterBattle(battleName):
    touch(mapper[battleName])

def done(exit=True):
    if exit:
        touch(mapper['close'])
    else:
        touch(mapper['continue'])
    
def castSkills(skills):
    '''
    一回合释放技能
    i : k 无目标技能，第i号从者的第k个技能
    i in (1, 2, 3), k in (1, 2, 3)
    i : (k, j) 有目标技能, 第i号从者的第k个技能对j号从者释放
    '''
    for k, v in skills.items():
        for i in v:
            if isinstance(i, int):
                servantSkill(k, i)
            else:
                servantSkill(k, i[0], i[1])

def summon(epoch=1):
    for _ in range(epoch):
        touch(wait(mapper['continueSummon'], intervalfunc=skip, interval=0.1))
        touch(mapper['yes'])
        sleep(1.5)

        
def skip():
    touch([0.85, 0.72])
    
    
def threeTurnBattle(battleName, skillSet, iterations=1):
    enterBattle(battleName)
    for i in range(iterations):
        chooseFriend()
        if i == 0:
            beginBattle()
        battleCore(skillSet)
        if i != iterations-1:
            done(False)
        else:
            done(True)

def battleCore(skillSet):
    '''
    2 3 3测试
    '''
    waitActionDone('attack_pic', timeout=60)
    castSkills(skillSet[0])
    masterSkill(1)
    attack()
    orderChange((3, 1))
    castSkills(skillSet[1])
    attack()
    castSkills(skillSet[2])
    masterSkill(1)
    attack(ifwait=False)
    waitActionDone(signal='battleFinish', timeout=40)
    battleFinish()
            

def battleCore1(skillSet):
    '''
    3 1 1
    '''
    waitActionDone('attack_pic', timeout=60)
    castSkills(skillSet[0])
    masterSkill(1)
    attack()
    castSkills(skillSet[1])
    orderChange((3, 1))
    castSkills(skillSet[2])
    attack(noble_idx=1)
    castSkills(skillSet[3])
    attack(noble_idx=1, ifwait=False)
    waitActionDone(signal='battleFinish', timeout=40)
    battleFinish()
    
    
skills = [{
    1: (1, (2, 2), (3, 2)),
    2: (1, ),
    3: (1, (2, 2),  (3, 2))
},
{
    2: (3, ),
    3: (2, 3),
},
{
    3: ((1, 2),) ,   
}
]

skills1 = [
{
    2: (3, ),
    3: (1, ),
},
{
    3: ((2, 1),),
    1: (2, 3),
},
{
    2: ((1, 1),),
    3: ((1, 1),),
},
{
    2: (2, (3, 1)),
    3: (2, (3, 1))
}
]
battleCore1(skills1)
# while True:
#     battleCore(skills)
#     done(False)
# threeTurnBattle('qp', skills, iterations=10)
# summon(500)