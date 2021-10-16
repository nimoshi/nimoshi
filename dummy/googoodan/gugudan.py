def myprint(_m, _n):
    print('{} * {} = {}'.format(_m, _n, _m * _n))

def main():
    print(f'my name is {__name__}')
    for i in range(1, 10):
        for j in range(1, 10):
            myprint(i, j)


if __name__ == '__main__':
    main()