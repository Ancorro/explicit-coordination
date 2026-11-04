from experiment import run

def test_repeatable():
    assert run('excel',3,4,8,20,True,7) == run('excel',3,4,8,20,True,7)

def test_ranges():
    for method in ('excel','hyq'):
        data=run(method,3,4,8,20,False,2)
        assert all(0 <= point['coordination'] <= 1 and 0 <= point['reward'] <= 9 for point in data['curve'])

def test_play_reset_coordinates_small_game():
    assert run('excel',3,5,32,3000,False,3,'play')['curve'][-1]['coordination'] > 0.9
