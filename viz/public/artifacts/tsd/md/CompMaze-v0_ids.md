```plantuml
strict digraph CompMaze { label="CompMaze-v0"
subgraph MAP {label=Map;map [shape=plaintext label=<<table border="1" cellpadding="5" cellspacing="0" cellborder="1"><tr><td bgcolor="0.39803922 0.15947579 0.99679532 1.        ">S:0</td><td bgcolor="0.35098039 0.23194764 0.99315867 1.        ">C:1</td><td bgcolor="0.29607843 0.31486959 0.98720184 1.        ">C:2</td><td bgcolor="0.24901961 0.38410575 0.98063477 1.        ">C:3</td></tr><tr><td bgcolor="0.19411765 0.46220388 0.97128103 1.        ">C:4</td><td bgcolor="0.14705882 0.52643216 0.96182564 1.        ">W:5</td><td bgcolor="0.09215686 0.59770746 0.94913494 1.        ">C:6</td><td bgcolor="0.0372549  0.66454018 0.93467977 1.        ">W:7</td></tr><tr><td bgcolor="0.00980392 0.71791192 0.92090552 1.        ">C:8</td><td bgcolor="0.06470588 0.77520398 0.9032472  1.        ">C:9</td><td bgcolor="0.11176471 0.81974048 0.88677369 1.        ">C:10</td><td bgcolor="0.16666667 0.8660254  0.8660254  1.        ">C:11</td></tr><tr><td bgcolor="0.21372549 0.9005867  0.84695821 1.        ">C:12</td><td bgcolor="0.26862745 0.93467977 0.82325295 1.        ">W:13</td><td bgcolor="0.32352941 0.96182564 0.79801723 1.        ">W:14</td><td bgcolor="0.37058824 0.97940977 0.77520398 1.        ">C:15</td></tr><tr><td bgcolor="0.4254902  0.99315867 0.74725253 1.        ">C:16</td><td bgcolor="0.47254902 0.99907048 0.72218645 1.        ">C:17</td><td bgcolor="0.52745098 0.99907048 0.69169844 1.        ">C:18</td><td bgcolor="0.5745098  0.99315867 0.66454018 1.        ">G:19</td></tr></table>>]} 
nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
subgraph cluster0 { label="Limit: 0" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"0_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "];  "#exp 1, #gen 1" [ shape=box ];
}
subgraph cluster1 { label="Limit: 1" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"1_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"1_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "1_0" -> "1_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"1_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "1_0" -> "1_0.4-3" [xlabel="(D,1)" headlabel=0];  "#exp 2, #gen 3" [ shape=box ];
}
subgraph cluster2 { label="Limit: 2" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"2_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"2_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "2_0" -> "2_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"2_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "2_0" -> "2_0.4-3" [xlabel="(D,1)" headlabel=0]; 
"2_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "];  "2_0.4-3" -> "2_0.4.8-3" [xlabel="(D,1)" headlabel=1];  "#exp 3, #gen 4" [ shape=box ];
}
subgraph cluster3 { label="Limit: 3" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"3_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"3_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "3_0" -> "3_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"3_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "3_0" -> "3_0.4-3" [xlabel="(D,1)" headlabel=0]; 
"3_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "];  "3_0.4-3" -> "3_0.4.8-3" [xlabel="(D,1)" headlabel=1]; 
"3_0.4.8.9-1" [label=9 style=filled color=white  fillcolor="0.06470588 0.77520398 0.9032472  1.        "];  "3_0.4.8-3" -> "3_0.4.8.9-1" [xlabel="(R,1)" headlabel=2]; 
"3_0.4.8.12-3" [label=12 style=filled color=white  fillcolor="0.21372549 0.9005867  0.84695821 1.        "];  "3_0.4.8-3" -> "3_0.4.8.12-3" [xlabel="(D,1)" headlabel=2];  "#exp 4, #gen 6" [ shape=box ];
}
subgraph cluster4 { label="Limit: 4" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"4_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"4_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "4_0" -> "4_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"4_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "4_0" -> "4_0.4-3" [xlabel="(D,1)" headlabel=0]; 
"4_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "];  "4_0.4-3" -> "4_0.4.8-3" [xlabel="(D,1)" headlabel=1]; 
"4_0.4.8.9-1" [label=9 style=filled color=white  fillcolor="0.06470588 0.77520398 0.9032472  1.        "];  "4_0.4.8-3" -> "4_0.4.8.9-1" [xlabel="(R,1)" headlabel=2]; 
"4_0.4.8.12-3" [label=12 style=filled color=white  fillcolor="0.21372549 0.9005867  0.84695821 1.        "];  "4_0.4.8-3" -> "4_0.4.8.12-3" [xlabel="(D,1)" headlabel=2]; 
"4_0.4.8.12.16-3" [label=16 style=filled color=white  fillcolor="0.4254902  0.99315867 0.74725253 1.        "];  "4_0.4.8.12-3" -> "4_0.4.8.12.16-3" [xlabel="(D,1)" headlabel=3];  "#exp 5, #gen 7" [ shape=box ];
}
subgraph cluster5 { label="Limit: 5" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"5_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"5_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "5_0" -> "5_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"5_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "5_0" -> "5_0.4-3" [xlabel="(D,1)" headlabel=0]; 
"5_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "];  "5_0.4-3" -> "5_0.4.8-3" [xlabel="(D,1)" headlabel=1]; 
"5_0.4.8.9-1" [label=9 style=filled color=white  fillcolor="0.06470588 0.77520398 0.9032472  1.        "];  "5_0.4.8-3" -> "5_0.4.8.9-1" [xlabel="(R,1)" headlabel=2]; 
"5_0.4.8.12-3" [label=12 style=filled color=white  fillcolor="0.21372549 0.9005867  0.84695821 1.        "];  "5_0.4.8-3" -> "5_0.4.8.12-3" [xlabel="(D,1)" headlabel=2]; 
"5_0.4.8.12.16-3" [label=16 style=filled color=white  fillcolor="0.4254902  0.99315867 0.74725253 1.        "];  "5_0.4.8.12-3" -> "5_0.4.8.12.16-3" [xlabel="(D,1)" headlabel=3]; 
"5_0.4.8.12.16.17-1" [label=17 style=filled color=white  fillcolor="0.47254902 0.99907048 0.72218645 1.        "];  "5_0.4.8.12.16-3" -> "5_0.4.8.12.16.17-1" [xlabel="(R,1)" headlabel=4];  "#exp 6, #gen 8" [ shape=box ];
}
subgraph cluster6 { label="Limit: 6" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"6_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"6_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "6_0" -> "6_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"6_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "];  "6_0" -> "6_0.4-3" [xlabel="(D,1)" headlabel=0]; 
"6_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "];  "6_0.4-3" -> "6_0.4.8-3" [xlabel="(D,1)" headlabel=1]; 
"6_0.4.8.9-1" [label=9 style=filled color=white  fillcolor="0.06470588 0.77520398 0.9032472  1.        "];  "6_0.4.8-3" -> "6_0.4.8.9-1" [xlabel="(R,1)" headlabel=2]; 
"6_0.4.8.12-3" [label=12 style=filled color=white  fillcolor="0.21372549 0.9005867  0.84695821 1.        "];  "6_0.4.8-3" -> "6_0.4.8.12-3" [xlabel="(D,1)" headlabel=2]; 
"6_0.4.8.12.16-3" [label=16 style=filled color=white  fillcolor="0.4254902  0.99315867 0.74725253 1.        "];  "6_0.4.8.12-3" -> "6_0.4.8.12.16-3" [xlabel="(D,1)" headlabel=3]; 
"6_0.4.8.12.16.17-1" [label=17 style=filled color=white  fillcolor="0.47254902 0.99907048 0.72218645 1.        "];  "6_0.4.8.12.16-3" -> "6_0.4.8.12.16.17-1" [xlabel="(R,1)" headlabel=4]; 
"6_0.4.8.12.16.17.18-1" [label=18 style=filled color=white  fillcolor="0.52745098 0.99907048 0.69169844 1.        "];  "6_0.4.8.12.16.17-1" -> "6_0.4.8.12.16.17.18-1" [xlabel="(R,1)" headlabel=5];  "#exp 7, #gen 9" [ shape=box ];
}
subgraph cluster7 { label="Limit: 7" nodesep=1 ranksep=0.5 node [shape=circle] edge [arrowsize=0.7] 
"7_0" [label=0 style=filled color=white  fillcolor="0.39803922 0.15947579 0.99679532 1.        "]; 
"7_0.1-1" [label=1 style=filled color=white  fillcolor="0.35098039 0.23194764 0.99315867 1.        "];  "7_0" -> "7_0.1-1" [xlabel="(R,1)" headlabel=0]; 
"7_0.4-3" [label=4 style=filled color=white  fillcolor="0.19411765 0.46220388 0.97128103 1.        "color=red color=red ];    "7_0" -> "7_0.4-3" [xlabel="(D,1)" headlabel=0color=red color=red ];   
"7_0.4.8-3" [label=8 style=filled color=white  fillcolor="0.00980392 0.71791192 0.92090552 1.        "color=red color=red ];    "7_0.4-3" -> "7_0.4.8-3" [xlabel="(D,1)" headlabel=1color=red color=red ];   
"7_0.4.8.9-1" [label=9 style=filled color=white  fillcolor="0.06470588 0.77520398 0.9032472  1.        "];  "7_0.4.8-3" -> "7_0.4.8.9-1" [xlabel="(R,1)" headlabel=2]; 
"7_0.4.8.12-3" [label=12 style=filled color=white  fillcolor="0.21372549 0.9005867  0.84695821 1.        "color=red color=red ];    "7_0.4.8-3" -> "7_0.4.8.12-3" [xlabel="(D,1)" headlabel=2color=red color=red ];   
"7_0.4.8.12.16-3" [label=16 style=filled color=white  fillcolor="0.4254902  0.99315867 0.74725253 1.        "color=red color=red ];    "7_0.4.8.12-3" -> "7_0.4.8.12.16-3" [xlabel="(D,1)" headlabel=3color=red color=red ];   
"7_0.4.8.12.16.17-1" [label=17 style=filled color=white  fillcolor="0.47254902 0.99907048 0.72218645 1.        "color=red color=red ];    "7_0.4.8.12.16-3" -> "7_0.4.8.12.16.17-1" [xlabel="(R,1)" headlabel=4color=red color=red ];   
"7_0.4.8.12.16.17.18-1" [label=18 style=filled color=white  fillcolor="0.52745098 0.99907048 0.69169844 1.        "color=red color=red ];    "7_0.4.8.12.16.17-1" -> "7_0.4.8.12.16.17.18-1" [xlabel="(R,1)" headlabel=5color=red color=red ];   
"7_0.4.8.12.16.17.18.19-1" [label=19 style=filled color=red peripheries=2 fillcolor="0.5745098  0.99315867 0.66454018 1.        "color=red color=red ];    "7_0.4.8.12.16.17.18-1" -> "7_0.4.8.12.16.17.18.19-1" [xlabel="(R,1)" headlabel=6color=red color=red ];   
 "#exp 8, #gen 10, cost:7" [ shape=box ];
}
 "#exp 36, #gen 48, cost:7" [ shape=box ];
}```
