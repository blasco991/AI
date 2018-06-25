```plantuml
strict digraph XSMaze { label="XSMaze-v0"
subgraph MAP {label=Map;map [shape=plaintext label=<<table border="1" cellpadding="5" cellspacing="0" cellborder="1"><tr><td bgcolor="0.32745098 0.267733   0.99083125 1.        ">S:0</td><td bgcolor="0.24117647 0.39545121 0.97940977 1.        ">C:1</td><td bgcolor="0.15490196 0.51591783 0.96349314 1.        ">C:2</td></tr><tr><td bgcolor="0.06862745 0.62692381 0.94315443 1.        ">C:3</td><td bgcolor="0.01764706 0.72643357 0.91848699 1.        ">W:4</td><td bgcolor="0.10392157 0.81262237 0.88960401 1.        ">C:5</td></tr><tr><td bgcolor="0.19803922 0.88960401 0.8534438  1.        ">C:6</td><td bgcolor="0.28431373 0.94315443 0.81619691 1.        ">W:7</td><td bgcolor="0.37058824 0.97940977 0.77520398 1.        ">C:8</td></tr><tr><td bgcolor="0.45686275 0.99770518 0.73065313 1.        ">C:9</td><td bgcolor="0.54313725 0.99770518 0.68274886 1.        ">C:10</td><td bgcolor="0.62941176 0.97940977 0.63171101 1.        ">G:11</td></tr></table>>]} 
nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
subgraph cluster0 { label="Limit: 0" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"0_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "];  "#exp 1, #gen 1" [ shape=box ];
}
subgraph cluster1 { label="Limit: 1" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"1_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "]; 
"1_0.1-1" [label=1 style=filled color=white  fillcolor="0.24117647 0.39545121 0.97940977 1.        "];  "1_0" -> "1_0.1-1" [label="(R,1)" ]; 
"1_0.3-3" [label=3 style=filled color=white  fillcolor="0.06862745 0.62692381 0.94315443 1.        "];  "1_0" -> "1_0.3-3" [label="(D,1)" ];  "#exp 2, #gen 3" [ shape=box ];
}
subgraph cluster2 { label="Limit: 2" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"2_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "]; 
"2_0.1-1" [label=1 style=filled color=white  fillcolor="0.24117647 0.39545121 0.97940977 1.        "];  "2_0" -> "2_0.1-1" [label="(R,1)" ]; 
"2_0.3-3" [label=3 style=filled color=white  fillcolor="0.06862745 0.62692381 0.94315443 1.        "];  "2_0" -> "2_0.3-3" [label="(D,1)" ]; 
"2_0.3.6-3" [label=6 style=filled color=white  fillcolor="0.19803922 0.88960401 0.8534438  1.        "];  "2_0.3-3" -> "2_0.3.6-3" [label="(D,1)" ];  "#exp 3, #gen 4" [ shape=box ];
}
subgraph cluster3 { label="Limit: 3" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"3_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "]; 
"3_0.1-1" [label=1 style=filled color=white  fillcolor="0.24117647 0.39545121 0.97940977 1.        "];  "3_0" -> "3_0.1-1" [label="(R,1)" ]; 
"3_0.3-3" [label=3 style=filled color=white  fillcolor="0.06862745 0.62692381 0.94315443 1.        "];  "3_0" -> "3_0.3-3" [label="(D,1)" ]; 
"3_0.3.6-3" [label=6 style=filled color=white  fillcolor="0.19803922 0.88960401 0.8534438  1.        "];  "3_0.3-3" -> "3_0.3.6-3" [label="(D,1)" ]; 
"3_0.3.6.9-3" [label=9 style=filled color=white  fillcolor="0.45686275 0.99770518 0.73065313 1.        "];  "3_0.3.6-3" -> "3_0.3.6.9-3" [label="(D,1)" ];  "#exp 4, #gen 5" [ shape=box ];
}
subgraph cluster4 { label="Limit: 4" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"4_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "]; 
"4_0.1-1" [label=1 style=filled color=white  fillcolor="0.24117647 0.39545121 0.97940977 1.        "];  "4_0" -> "4_0.1-1" [label="(R,1)" ]; 
"4_0.3-3" [label=3 style=filled color=white  fillcolor="0.06862745 0.62692381 0.94315443 1.        "];  "4_0" -> "4_0.3-3" [label="(D,1)" ]; 
"4_0.3.6-3" [label=6 style=filled color=white  fillcolor="0.19803922 0.88960401 0.8534438  1.        "];  "4_0.3-3" -> "4_0.3.6-3" [label="(D,1)" ]; 
"4_0.3.6.9-3" [label=9 style=filled color=white  fillcolor="0.45686275 0.99770518 0.73065313 1.        "];  "4_0.3.6-3" -> "4_0.3.6.9-3" [label="(D,1)" ]; 
"4_0.3.6.9.10-1" [label=10 style=filled color=white  fillcolor="0.54313725 0.99770518 0.68274886 1.        "];  "4_0.3.6.9-3" -> "4_0.3.6.9.10-1" [label="(R,1)" ];  "#exp 5, #gen 6" [ shape=box ];
}
subgraph cluster5 { label="Limit: 5" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"5_0" [label=0 style=filled color=white  fillcolor="0.32745098 0.267733   0.99083125 1.        "]; 
"5_0.1-1" [label=1 style=filled color=white  fillcolor="0.24117647 0.39545121 0.97940977 1.        "];  "5_0" -> "5_0.1-1" [label="(R,1)" ]; 
"5_0.3-3" [label=3 style=filled color=white  fillcolor="0.06862745 0.62692381 0.94315443 1.        "color=red color=red ];    "5_0" -> "5_0.3-3" [label="(D,1)" color=red color=red ];   
"5_0.3.6-3" [label=6 style=filled color=white  fillcolor="0.19803922 0.88960401 0.8534438  1.        "color=red color=red ];    "5_0.3-3" -> "5_0.3.6-3" [label="(D,1)" color=red color=red ];   
"5_0.3.6.9-3" [label=9 style=filled color=white  fillcolor="0.45686275 0.99770518 0.73065313 1.        "color=red color=red ];    "5_0.3.6-3" -> "5_0.3.6.9-3" [label="(D,1)" color=red color=red ];   
"5_0.3.6.9.10-1" [label=10 style=filled color=white  fillcolor="0.54313725 0.99770518 0.68274886 1.        "color=red color=red ];    "5_0.3.6.9-3" -> "5_0.3.6.9.10-1" [label="(R,1)" color=red color=red ];   
"5_0.3.6.9.10.11-1" [label=11 style=filled color=red peripheries=2 fillcolor="0.62941176 0.97940977 0.63171101 1.        "color=red color=red ];    "5_0.3.6.9.10-1" -> "5_0.3.6.9.10.11-1" [label="(R,1)" color=red color=red ];   
 "#exp 6, #gen 7, cost:5" [ shape=box ];
}
 "#exp 21, #gen 26, cost:5" [ shape=box ];
}```
