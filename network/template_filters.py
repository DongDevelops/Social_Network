from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    list = []
    for i in dictionary:
        a = i.like_user
        list.append(a)

    count = 0
    for item in list:
        if item == key:
            count = count + 1
            break
        else:
            pass
    return count



@register.filter
def lookup(dictionary, key):
    list = []
    for i in dictionary:
        a = i.follower
        list.append(a)

    count = 0
    for item in list:
        if item == key:
            count = count + 1
            break
        else:
            pass
    return count
