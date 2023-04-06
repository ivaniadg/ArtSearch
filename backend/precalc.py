from pose_matching import op_utils as op
from color_matching import cm_utils as cm
from object_detection import od_utils as od


img = "antoine-watteau_the-flautist.jpg"


# _, res = op.get_precalc_pose_score(img)
#sort dict by value
# res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
# print(res)


# x = od.get_precalc_scores(img)

x = cm.load_data()

y =  x[img]

print(y)