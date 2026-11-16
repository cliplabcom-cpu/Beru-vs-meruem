import sys; sys.path.insert(0,'.')
import scene_street as ss, kit, chars
def a4(save, cam=None, clock_x=1.6):
    cam=cam or dict(pos=(-3.4,1.7,-14.5),yaw=0,pitch=2.0,hfov=66)
    R=ss.render_street(1,'main',cam=cam,clock_x=clock_x,tree_x=-0.1,lamps=(-8.9,),planters=False,near_bin=False)
    chars.place(R,'sam_front',-4.1,-7.3)
    chars.place(R,'asha_front',-2.6,-7.3)
    chars.place(R,'emeka_front',-1.0,-7.3)
    if save: kit.grade(R.finish()).save(save)
    return R
if __name__=='__main__':
    SP='/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    R=a4(SP+'a4_test.png'); print(R.boxes)
