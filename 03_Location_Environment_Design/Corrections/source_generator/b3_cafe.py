import sys; sys.path.insert(0,'.')
import scene_cafe as sc, kit, chars
def b3(save, cam=None):
    def behind(R):
        chars.place(R,'asha_apron_front',sc.ASHA_X,7.0,op=0.0,shadow=False)
    R=sc.render(cam or sc.cam_b1(),plan=sc.plan_b3(),behind=behind,pendants=((-1.6,4.2),(0.4,3.9),(1.9,4.5)))
    # customers are drawn after the room (nearer than Asha) - composited on top, then lamps stay above heads
    chars.place(R,'emeka_side',-2.0,5.0)
    chars.place(R,'sam_front',-3.0,4.3)
    if save: kit.grade(R.finish(),vig=0.08).save(save)
    return R
if __name__=='__main__':
    SP='/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    R=b3(SP+'b3_test.png'); print(R.boxes)
