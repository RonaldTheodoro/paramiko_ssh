import argparse
from access import SSH


def access_ssh(ip, cpf, discount):
    if discount == 'f':
        arq = 'cpfesc'

    elif discount == 'a':
        arq = 'cpf'

    conn = SSH(ip)

    try:
        conn.sendCommand('echo "{}" > /siga/sisloja/{}.txt'.format(cpf, arq))
    except TimeoutError:
        print('Is not possible access the ip {}'.format(ip))
    else:
        print('CPF cadastrado com sucesso')


def menu(args):
    args.ip = input('Digite o ip: ')
    args.cpf = input('Digite o CPF: ')
    print('Selecione o tipo de desconto', end=' ')
    discount = input('(Aniversariante: a ou Funcionario: f): ')

    if discount == 'a':
        args.birthday = True
        args.employee = False

    elif discount == 'f':
        args.birthday = False
        args.employee = True

    main(args)


def main(args):
    if args.ip is None:
        print('You must enter the ip')

    elif args.cpf is None:
        print('You must enter the cpf')

    elif args.birthday and args.employee:
        print('You can\'t choice both')

    elif args.birthday:
        access_ssh(args.ip, args.cpf, 'a')

    elif args.employee:
        access_ssh(args.ip, args.cpf, 'f')
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CPF register')
    parser.add_argument('-ip', help='Enter the ip', type=str)
    parser.add_argument('-cpf', help='Enter the cpf', type=str)
    parser.add_argument(
        '-e', 
        '--employee', 
        help='discount for employee', 
        action='store_true', 
        default=False
    )
    parser.add_argument(
        '-b', 
        '--birthday', 
        help='discount for birthday', 
        action='store_true', 
        default=False
    )

    args = parser.parse_args()

    if args.ip is None:
        menu(args)

    else:
        main(args)

