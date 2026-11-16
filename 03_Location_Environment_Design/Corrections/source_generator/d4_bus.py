import sys; sys.path.insert(0, '.')
import scene_bus as sb, kit, chars
SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
# Sam & Emeka flank the aisle at near-equal depth (true height ratio readable); Asha stands further ahead in the centre line.
POS = dict(sam=(0.38, 8.4), emeka=(0.85, 6.9), asha=(-0.28, 6.3))


def d4(save=None, pos=POS, cam=None):
    def put(R):
        chars.place(R, 'sam_side', *pos['sam'])
        chars.place(R, 'emeka_side', *pos['emeka'], flip=True)
        chars.place(R, 'asha_front', *pos['asha'])
    R = sb.render('d4', cam=cam, behind=put, split_z=pos['asha'][1] - 0.5)
    if save: kit.grade(R.finish(), vig=0.08).save(save)
    return R
if __name__ == '__main__':
    R = d4(SP + 'd4_test.png'); print(R.boxes)
