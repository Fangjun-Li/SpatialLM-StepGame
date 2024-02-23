def get_task(name):
    if name == 'game24':
        from tot.tasks.game24 import Game24Task
        return Game24Task()
    elif name == 'text':
        from tot.tasks.text import TextTask
        return TextTask()
    elif name == 'crosswords':
        from tot.tasks.crosswords import MiniCrosswordsTask
        return MiniCrosswordsTask()
    elif 'stepgame' in name:
        from tot.tasks.stepgame import StepgameTask
        return StepgameTask(file= 'qa'+ name.split('_')[1]+'_test.txt')
    else:
        raise NotImplementedError