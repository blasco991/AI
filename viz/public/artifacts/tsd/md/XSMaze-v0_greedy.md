```plantuml
digraph XSMaze { label="XSMaze-v0"
subgraph MAP {label=Map;map [shape=plaintext label=<<table border="1" cellpadding="5" cellspacing="0" cellborder="1"><tr><td bgcolor="0.32745098 0.267733   0.99083125 1.        ">S:0</td><td bgcolor="0.24117647 0.39545121 0.97940977 1.        ">C:1</td><td bgcolor="0.15490196 0.51591783 0.96349314 1.        ">C:2</td></tr><tr><td bgcolor="0.06862745 0.62692381 0.94315443 1.        ">C:3</td><td bgcolor="0.01764706 0.72643357 0.91848699 1.        ">W:4</td><td bgcolor="0.10392157 0.81262237 0.88960401 1.        ">C:5</td></tr><tr><td bgcolor="0.19803922 0.88960401 0.8534438  1.        ">C:6</td><td bgcolor="0.28431373 0.94315443 0.81619691 1.        ">W:7</td><td bgcolor="0.37058824 0.97940977 0.77520398 1.        ">C:8</td></tr><tr><td bgcolor="0.45686275 0.99770518 0.73065313 1.        ">C:9</td><td bgcolor="0.54313725 0.99770518 0.68274886 1.        ">C:10</td><td bgcolor="0.62941176 0.97940977 0.63171101 1.        ">G:11</td></tr></table>>]} 
nodesep=1 ranksep=0.5 node [shape=record] edge [arrowsize=0.7] 
"0_0" [label="<f0>0 |<f1> cost: 0" style=filled color=white fillcolor="0.32745098 0.267733   0.99083125 1.        "]
"0_0.1-1" [label="<f0>1 |<f1> cost: 1" style=filled color=white fillcolor="0.24117647 0.39545121 0.97940977 1.        "] "0_0" -> "0_0.1-1" [xlabel="(R,1)" headlabel=0color=red ];  
"0_0.3-3" [label="<f0>3 |<f1> cost: 1" style=filled color=white fillcolor="0.06862745 0.62692381 0.94315443 1.        "] "0_0" -> "0_0.3-3" [xlabel="(D,1)" headlabel=0]; 
"0_0.1.2-1" [label="<f0>2 |<f1> cost: 2" style=filled color=white fillcolor="0.15490196 0.51591783 0.96349314 1.        "] "0_0.1-1" -> "0_0.1.2-1" [xlabel="(R,1)" headlabel=1color=red ];  
"0_0.1.2.5-3" [label="<f0>5 |<f1> cost: 3" style=filled color=white fillcolor="0.10392157 0.81262237 0.88960401 1.        "] "0_0.1.2-1" -> "0_0.1.2.5-3" [xlabel="(D,1)" headlabel=2color=red ];  
"0_0.1.2.5.8-3" [label="<f0>8 |<f1> cost: 4" style=filled color=white fillcolor="0.37058824 0.97940977 0.77520398 1.        "] "0_0.1.2.5-3" -> "0_0.1.2.5.8-3" [xlabel="(D,1)" headlabel=3color=red ];  
"0_0.1.2.5.8.11-3" [label="<f0>11 |<f1> cost: 5" style=filled color=red fillcolor="0.62941176 0.97940977 0.63171101 1.        "] "0_0.1.2.5.8-3" -> "0_0.1.2.5.8.11-3" [xlabel="(D,1)" headlabel=4color=red ];  
 "#exp 6, #gen 7, cost:5" [ shape=box ];
}```
