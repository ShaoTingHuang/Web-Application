from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'calculator.html',{})

def button(request):
    context = {}
    try:
        count=int(request.GET['count'])
    except:
        count=0
    try:
        new_val=int(request.GET['newVal'])
    except:
        new_val=0
    try:
        prev_val=int(request.GET['prevVal'])
    except:
        prev_val=0
    try:
        result=int(request.GET['result'])
    except:
        result=0
    if request.GET['prevOp'] not in set(['plus','minus','times','divides','equals']):
        prev_op = 'plus'
    else:
        prev_op = request.GET['prevOp']

    if 'val' in request.GET:
        new_val *= 10
        new_val += int(request.GET['val'])
        result = new_val
        count = 0
    else:
        if count == 0:
            if request.GET['prevOp'] == 'equals':
                result = prev_val
                new_val = 0
                prev_op = request.GET['op']
            elif request.GET['prevOp'] == 'divides':
                if (new_val == 0):
                    result = 'err'
                    prev_val = 0
                else :
                    prev_val = prev_val / new_val
                    result = prev_val
                new_val = 0
                prev_op = request.GET['op']
            else:
                if request.GET['prevOp'] == 'plus':
                    prev_val = prev_val + new_val
                if request.GET['prevOp'] == 'minus':
                    prev_val = prev_val - new_val
                if request.GET['prevOp'] == 'times':
                    prev_val = prev_val * new_val
                new_val = 0
                prev_op = request.GET['op']
                result = prev_val
        else:
            count += 1
            prev_op = request.GET['op']
            result = prev_val
    print str(result) + " " + str(prev_val) + " " + str(new_val) + " " + prev_op
    context = {'result':result, 'prevVal':prev_val, 'newVal':new_val, 'prevOp':prev_op, 'count':count}
    return render(request, 'calculator.html', context)
