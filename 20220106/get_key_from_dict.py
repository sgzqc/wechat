import pandas as pd


if __name__ == "__main__":
    currency_dict = {'USD': 'Dollar',
                     'EUR': 'Euro',
                     ' GBP': 'Pound',
                     'CNY': 'Chinese'}

    # way 1
    key_list = list(currency_dict.keys())
    val_list = list(currency_dict.values())
    val = 'Chinese'
    ind = val_list.index(val)
    print(key_list[ind])

    # way 2
    def return_key(val):
        for i in range(len(currency_dict)):
            if val_list[i] == val:
                return key_list[i]
        return ("Key Not Found")

    print(return_key("Dollar"))

    # way 3
    def return_key2(val):
        for key, value in currency_dict.items():
            if value == val:
                return key
        return ('Key Not Found')

    print(return_key2('Euro'))


    # way 4
    df = pd.DataFrame({'abbr': list(currency_dict.keys()),
                       'curr': list(currency_dict.values())})
    val = 'Pound'
    print(df.abbr[df.curr == val])
    print(df.abbr[df.curr == val].unique()[0])
    print(df.abbr[df.curr == val].mode()[0])
    print(df.abbr[df.curr == val].sum())




