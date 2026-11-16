import sys; sys.path.insert(0,'.')
import scene_market as sm, kit, chars
def c3(save, cam=None):
    cam = cam or dict(pos=(0.0, 1.5, -7.6), yaw=0.0, pitch=1.0, hfov=60.0)
    def behind(R):
        chars.place(R, 'asha_apron_front', 0.62, 0.95, shadow=False)
    R = sm.render('c1', cam=cam, behind=behind)
    chars.place(R, 'emeka_side', -2.95, -0.3)
    chars.place(R, 'sam_side', 2.5, -0.5, flip=True)
    if save: kit.grade(R.finish()).save(save)
    return R
if __name__ == '__main__':
    SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    R = c3(SP + 'c3_test.png'); print(R.boxes)
