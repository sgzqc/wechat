import pandas as pd
import json


def test0():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)
        print(type(superHeroSquad))
        print(superHeroSquad.keys())


def test1():
    df = pd.read_json('superheroes.json')
    df = pd.concat([df['members'].apply(pd.Series), df.drop('members', axis=1)], axis=1)
    print(df)


def test2():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)
    out = pd.json_normalize(superHeroSquad, record_path=['members'],
                      meta=['squadName', 'homeTown', 'formed', 'secretBase', 'active'])
    print(out)


def test3():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)
        print(superHeroSquad['members'][1]['secretIdentity'])

def test4():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)

    superHeroSquad['members'][2]['secretIdentity'] = 'Will Smith'
    with open('superheroes2.json', 'w') as file:
        json.dump(superHeroSquad, file)


def test5():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)

    superHeroSquad['members'][2]['secretIdentity'] = 'Will Smith'
    with open('superheroes3.json', 'w') as file:
        json.dump(superHeroSquad, file, indent = 4)


def test6():
    with open('superheroes.json') as f:
        superHeroSquad = json.load(f)

    superHeroSquad['members'][2]['secretIdentity'] = 'Will Smith'
    with open('superheroes4.json', 'w') as file:
        json.dump(superHeroSquad, file, indent = 4,sort_keys = True)



if __name__ == "__main__":
    #test0()
    #test1()
    #test2()
    #test3()
    #test4()
    #test5()
    test6()


