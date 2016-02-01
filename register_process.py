import sys


def register_process(file_name, name):
    fileinput = open('/etc/init.d/skeleton', 'r')
    file = open(file_name, 'w')

    for line in fileinput.read().split('\n'):

        if line == 'NAME=daemonexecutablename':
            print(line)
            file.writelines("NAME=" + name + "\n")
        else:
            file.writelines(line+'\n')
    fileinput.close()
    file.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        name = sys.argv[2]
        register_process(file_name, name)
    else:
        print('Missing file name!')
