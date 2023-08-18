1. 内部有四个红凳子围成一个圈，然后外面是绿椅子围成两个圈，最中间是一个桌子。

   inside were four red stools enclosed in a circle, then outside were green chairs enclosed in two circles, with a table in the middle.

   ```
   Entity count: 5
   entity: stools-5 (plural)
     attributes: inside,red,
     count: 4
     relationships: enclosed in:circle-9,
   
   entity: circle-9
     determiners: a,
   
   entity: chairs-15 (plural)
     attributes: outside,green,then,
     relationships: enclosed in:circles-19,enclosed with:table-23,
   
   entity: circles-19 (plural)
     count: 2
   
   entity: table-23
     attributes: middle,
     determiners: a,
   ```

   nsubj(stools-5, inside-1~IN)
   cop(stools-5, were-2~VBD)
   nummod(stools-5, four-3~CD)
   amod(stools-5, red-4~JJ)
   root(root-0, stools-5~NNS)
   acl(stools-5, enclosed-6~VBN)
   case(circle-9, in-7~IN)
   det(circle-9, a-8~DT)
   nmod:in(enclosed-6, circle-9~NN)
   punct(stools-5, ,-10~,)
   advmod(chairs-15, then-11~RB)
   nsubj(chairs-15, outside-12~JJ)
   cop(chairs-15, were-13~VBD)
   amod(chairs-15, green-14~JJ)
   parataxis(stools-5, chairs-15~NNS)
   acl(chairs-15, enclosed-16~VBN)
   case(circles-19, in-17~IN)
   nummod(circles-19, two-18~CD)
   nmod:in(enclosed-16, circles-19~NNS)
   punct(enclosed-16, ,-20~,)
   case(table-23, with-21~IN)
   det(table-23, a-22~DT)
   nmod:with(enclosed-16, table-23~NN)
   case(middle-26, in-24~IN)
   det(middle-26, the-25~DT)
   nmod:in(table-23, middle-26~NN)
   punct(stools-5, .-27~.)

2. 绿色椅子围着四个红色沙发，然后沙发中间有一个小桌子。

   绿色椅子围着四个（皮质的）红色沙发，然后沙发中间有一个小桌子。

   The green chairs surrounded the four red leather sofas, and then there was a small table in the middle of the sofa.

   ```
   Entity count: 4
   entity: chairs-3 (plural)
     attributes: surrounded,green,
     determiners: the,
     relationships: surrounded:sofas-9,
   
   entity: sofas-9 (plural)
     attributes: leather,red,
     count: 4
     determiners: the,
   
   entity: table-17
     attributes: was(then),small,middle,
     determiners: a,
     relationships: in middle of:sofa-23,
   
   entity: sofa-23
     determiners: the,
   ```

   det(chairs-3, the-1~DT)
   amod(chairs-3, green-2~JJ)
   nsubj(surrounded-4, chairs-3~NNS)
   root(root-0, surrounded-4~VBD)
   det(sofas-9, the-5~DT)
   nummod(sofas-9, four-6~CD)
   amod(sofas-9, red-7~JJ)
   compound(sofas-9, leather-8~NN)
   dobj(surrounded-4, sofas-9~NNS)
   punct(surrounded-4, ,-10~,)
   cc(surrounded-4, and-11~CC)
   advmod(was-14, then-12~RB)
   expl(was-14, there-13~EX)
   conj:and(surrounded-4, was-14~VBD)
   det(table-17, a-15~DT)
   amod(table-17, small-16~JJ)
   nsubj(was-14, table-17~NN)
   case(middle-20, in-18~IN)
   det(middle-20, the-19~DT)
   nmod:in(table-17, middle-20~NN)
   case(sofa-23, of-21~IN)
   det(sofa-23, the-22~DT)
   nmod:of(middle-20, sofa-23~NN)
   punct(surrounded-4, .-24~.)

3. 以四张方形小沙发为中心，绿色椅子层层环绕，围绕成两圈。

   With four small square sofas as the center, the green chairs are surrounded by layers and are circled in two circles.

   ```
   Entity count: 4
   entity: sofas-5 (plural)
     attributes: small,square,center,
     count: 4
   
   entity: chairs-12 (plural)
     attributes: circled,green,
     determiners: the,
     relationships: circled in:circles-22,
   
   entity: layers-16 (plural)
   
   entity: circles-22 (plural)
     count: 2
   ```

   case(sofas-5, with-1~IN)
   nummod(sofas-5, four-2~CD)
   amod(sofas-5, small-3~JJ)
   amod(sofas-5, square-4~JJ)
   nmod:with(surrounded-14, sofas-5~NNS)
   case(center-8, as-6~IN)
   det(center-8, the-7~DT)
   nmod:as(sofas-5, center-8~NN)
   punct(surrounded-14, ,-9~,)
   det(chairs-12, the-10~DT)
   amod(chairs-12, green-11~JJ)
   nsubjpass(circled-19, chairs-12~NNS)
   auxpass(surrounded-14, are-13~VBP)
   root(root-0, surrounded-14~VBN)
   case(layers-16, by-15~IN)
   nmod:agent(surrounded-14, layers-16~NNS)
   cc(surrounded-14, and-17~CC)
   auxpass(circled-19, are-18~VBP)
   conj:and(surrounded-14, circled-19~VBN)
   case(circles-22, in-20~IN)
   nummod(circles-22, two-21~CD)
   nmod:in(circled-19, circles-22~NNS)
   punct(surrounded-14, .-23~.)

4. 围绕一张小桌子和五把椅子，几十张椅子围绕中心点向四周呈射线式分散。

   Around a small table and five chairs, dozens of chairs radially scattered around the center point.

   ```
   Entity count: 5
   entity: table-4
     attributes: small,
     determiners: a,
   
   entity: chairs-7 (plural)
     count: 5
   
   entity: dozens-9 (plural)
   
   entity: chairs-11 (plural)
     attributes: scattered(radially),
     determiners: dozens,
     relationships: scattered around:table-4,scattered around:chairs-7,scattered around:point-17,
   
   entity: point-17
     attributes: center,
     determiners: the,
   ```

   case(table-4, around-1~IN)
   det(table-4, a-2~DT)
   amod(table-4, small-3~JJ)
   nmod:around(scattered-13, table-4~NN)
   cc(table-4, and-5~CC)
   nummod(chairs-7, five-6~CD)
   nmod:around(scattered-13, chairs-7~NNS)
   punct(scattered-13, ,-8~,)
   det:qmod(chairs-11, dozens-9~NNS)
   mwe(dozens-9, of-10~IN)
   nsubj(scattered-13, chairs-11~NNS)
   advmod(scattered-13, radially-12~RB)
   root(root-0, scattered-13~VBN)
   case(point-17, around-14~IN)
   det(point-17, the-15~DT)
   compound(point-17, center-16~NN)
   nmod:around(scattered-13, point-17~NN)
   punct(scattered-13, .-18~.)

5. 几张小桌围绕一个圆桌。

   There are several small tables around a round table.

   ```
   Entity count: 2
   entity: tables-5 (plural)
     attributes: small,table,
     count: several
     relationships: around:table-9,
   
   entity: table-9
     attributes: round,
     determiners: a,
   ```

   expl(are-2, there-1~EX)
   root(root-0, are-2~VBP)
   amod(tables-5, several-3~JJ)
   amod(tables-5, small-4~JJ)
   nsubj(are-2, tables-5~NNS)
   case(table-9, around-6~IN)
   det(table-9, a-7~DT)
   compound(table-9, round-8~NN)
   nmod:around(tables-5, table-9~NN)
   punct(are-2, .-10~.)

6. 椅子围绕中心圆形放置逐渐向外扩展，最内圈是五把黄色的椅子，外围是黑色的椅子。

   The chair is gradually extended outward around the center circle, the inner ring is five yellow chairs, and the periphery is a black chair.

   ```
   Entity count: 6
   entity: chair-2
     attributes: extended(gradually),
     determiners: the,
   
   entity: circle-10
     attributes: center,
     determiners: the,
   
   entity: ring-14
     attributes: inner,
     determiners: the,
   
   entity: chairs-18 (plural)
     attributes: ring-14,yellow,
     count: 5
   
   entity: periphery-22
     determiners: the,
   
   entity: chair-26
     attributes: periphery-22,black,
     determiners: a,
   ```

   det(chair-2, the-1~DT)
   nsubjpass(extended-5, chair-2~NN)
   auxpass(extended-5, is-3~VBZ)
   advmod(extended-5, gradually-4~RB)
   root(root-0, extended-5~VBN)
   dep(extended-5, outward-6~JJ)
   case(circle-10, around-7~IN)
   det(circle-10, the-8~DT)
   compound(circle-10, center-9~NN)
   nmod:around(outward-6, circle-10~NN)
   punct(chairs-18, ,-11~,)
   det(ring-14, the-12~DT)
   amod(ring-14, inner-13~JJ)
   nsubj(chairs-18, ring-14~NN)
   cop(chairs-18, is-15~VBZ)
   nummod(chairs-18, five-16~CD)
   amod(chairs-18, yellow-17~JJ)
   dep(extended-5, chairs-18~NNS)
   punct(chairs-18, ,-19~,)
   cc(extended-5, and-20~CC)
   det(periphery-22, the-21~DT)
   nsubj(chair-26, periphery-22~NN)
   cop(chair-26, is-23~VBZ)
   det(chair-26, a-24~DT)
   amod(chair-26, black-25~JJ)
   conj:and(extended-5, chair-26~NN)
   punct(extended-5, .-27~.)

7. 外圈围绕着一圈小型书桌，每张书桌配有一张椅子，内圈有六张椅子围绕着一张大圆桌。

   The outer circle is surrounded by a circle of small desks, each with a chair, and the inner circle is surrounded by six chairs around a large round table.

   ```
   Entity count: 7
   entity: circle-3
     attributes: surrounded,outer,
     determiners: the,
     relationships: surrounded agent:circle-8,surrounded with:chair-16,agent a circle of:desks-11,
   
   entity: circle-8
     attributes: desks,
     determiners: a,
     relationships: of:desks-11,
   
   entity: desks-11 (plural)
     attributes: small,
   
   entity: chair-16
     determiners: a,
   
   entity: circle-21
     attributes: surrounded,inner,
     determiners: the,
     relationships: surrounded agent:chairs-26,agent chairs around:table-31,
   
   entity: chairs-26 (plural)
     attributes: table,
     count: 6
     relationships: around:table-31,
   
   entity: table-31
     attributes: round,large,
     determiners: a,
   ```

   det(circle-3, the-1~DT)
   amod(circle-3, outer-2~JJ)
   nsubjpass(surrounded-5, circle-3~NN)
   auxpass(surrounded-5, is-4~VBZ)
   root(root-0, surrounded-5~VBN)
   case(circle-8, by-6~IN)
   det(circle-8, a-7~DT)
   nmod:agent(surrounded-5, circle-8~NN)
   case(desks-11, of-9~IN)
   amod(desks-11, small-10~JJ)
   nmod:of(circle-8, desks-11~NNS)
   punct(circle-8, ,-12~,)
   advmod(circle-8, each-13~DT)
   case(chair-16, with-14~IN)
   det(chair-16, a-15~DT)
   nmod:with(surrounded-5, chair-16~NN)
   punct(surrounded-5, ,-17~,)
   cc(surrounded-5, and-18~CC)
   det(circle-21, the-19~DT)
   amod(circle-21, inner-20~JJ)
   nsubjpass(surrounded-23, circle-21~NN)
   auxpass(surrounded-23, is-22~VBZ)
   conj:and(surrounded-5, surrounded-23~VBN)
   case(chairs-26, by-24~IN)
   nummod(chairs-26, six-25~CD)
   nmod:agent(surrounded-23, chairs-26~NNS)
   case(table-31, around-27~IN)
   det(table-31, a-28~DT)
   amod(table-31, large-29~JJ)
   compound(table-31, round-30~NN)
   nmod:around(chairs-26, table-31~NN)
   punct(surrounded-5, .-32~.)

8. 外圈两排椅子围绕着内圈的四张沙发，其中两张沙发之间有一个小圆桌。

   Two rows of chairs surround the four sofas in the inner ring, with a small round table between the two sofas.

   ```
   Entity count: 6
   entity: rows-2 (plural)
     attributes: surround,chairs,
     count: 2
     relationships: of:chairs-4,surround with:table-18,surround:sofas-8,with a table between:sofas-22,
   
   entity: chairs-4 (plural)
   
   entity: sofas-8 (plural)
     attributes: ring,
     count: 4
     determiners: the,
     relationships: in:ring-12,with:table-18,
   
   entity: ring-12
     attributes: inner,
     determiners: the,
   
   entity: table-18
     attributes: round,small,sofas,
     determiners: a,
     relationships: between:sofas-22,
   
   entity: sofas-22 (plural)
     count: 2
     determiners: the,
   ```

   nummod(rows-2, two-1~CD)
   nsubj(surround-5, rows-2~NNS)
   case(chairs-4, of-3~IN)
   nmod:of(rows-2, chairs-4~NNS)
   root(root-0, surround-5~VBP)
   det(sofas-8, the-6~DT)
   nummod(sofas-8, four-7~CD)
   dobj(surround-5, sofas-8~NNS)
   case(ring-12, in-9~IN)
   det(ring-12, the-10~DT)
   amod(ring-12, inner-11~JJ)
   nmod:in(sofas-8, ring-12~NN)
   punct(surround-5, ,-13~,)
   case(table-18, with-14~IN)
   det(table-18, a-15~DT)
   amod(table-18, small-16~JJ)
   compound(table-18, round-17~NN)
   nmod:with(surround-5, table-18~NN)
   case(sofas-22, between-19~IN)
   det(sofas-22, the-20~DT)
   nummod(sofas-22, two-21~CD)
   nmod:between(table-18, sofas-22~NNS)
   punct(surround-5, .-23~.)

9. 里外有几层座位，环环围绕成一个圈，没有桌子只有椅子，间距不一，较为随意。

   There are several layers of seats inside and outside, the ring is surrounded by a circle, there is no table but a chair, the spacing is different, more casual.

   ```
   Entity count: 6
   entity: layers-4 (plural)
     attributes: seats,
     count: several
     relationships: of:seats-6,
   
   entity: seats-6 (plural)
   
   entity: ring-12
     attributes: surrounded,
     determiners: the,
     relationships: surrounded agent:circle-17,
   
   entity: circle-17
     determiners: a,
   
   entity: chair-25
     determiners: a,
   
   entity: spacing-28
     attributes: different,
     determiners: the,
   ```

   expl(are-2, there-1~EX)
   root(root-0, are-2~VBP)
   amod(layers-4, several-3~JJ)
   nsubj(are-2, layers-4~NNS)
   case(seats-6, of-5~IN)
   nmod:of(layers-4, seats-6~NNS)
   advmod(are-2, inside-7~IN)
   cc(inside-7, and-8~CC)
   conj:and(inside-7, outside-9~IN)
   punct(are-2, ,-10~,)
   det(ring-12, the-11~DT)
   nsubjpass(surrounded-14, ring-12~NN)
   auxpass(surrounded-14, is-13~VBZ)
   parataxis(are-2, surrounded-14~VBN)
   case(circle-17, by-15~IN)
   det(circle-17, a-16~DT)
   nmod:agent(surrounded-14, circle-17~NN)
   punct(are-2, ,-18~,)
   expl(is-20, there-19~EX)
   parataxis(are-2, is-20~VBZ)
   neg(table-22, no-21~DT)
   nsubj(is-20, table-22~NN)
   case(chair-25, but-23~CC)
   det(chair-25, a-24~DT)
   nmod:but(table-22, chair-25~NN)
   punct(are-2, ,-26~,)
   det(spacing-28, the-27~DT)
   nsubj(different-30, spacing-28~NN)
   cop(different-30, is-29~VBZ)
   parataxis(are-2, different-30~JJ)
   punct(different-30, ,-31~,)
   advmod(casual-33, more-32~RBR)
   dep(different-30, casual-33~JJ)
   punct(are-2, .-34~.)

10. 椅子呈圆形排成三排，每个椅子都有一个桌子。最中间是三把椅子和一个桌子。

    The chairs are arranged in three rows in a circle, and each chair has a table, with three chairs and a table in the middle.

    ```
    Entity count: 7
    entity: chairs-2 (plural)
      attributes: arranged,
      determiners: the,
      relationships: arranged in:rows-7,in rows in:circle-10,
    
    entity: rows-7 (plural)
      attributes: circle,
      count: 3
      relationships: in:circle-10,
    
    entity: circle-10
      determiners: a,
    
    entity: chair-14
      attributes: has,
      determiners: each,
      relationships: has with:chairs-21,has:table-17,
    
    entity: table-17
      determiners: a,
      relationships: with:chairs-21,
    
    entity: chairs-21 (plural)
      count: 3
    
    entity: table-24
      attributes: middle,
      determiners: a,
    ```

    



on the outside are 10 chairs in each circle.

```
case(outside-3, on-1~IN)
det(outside-3, the-2~DT)
nmod:on(are-4, outside-3~NN)
root(root-0, are-4~VBP)
nummod(chairs-6, 10-5~CD)
nsubj(are-4, chairs-6~NNS)
case(circle-9, in-7~IN)
det(circle-9, each-8~DT)
nmod:in(chairs-6, circle-9~NN)
punct(are-4, .-10~.)

Entity count: 3
entity: outside-3
  determiners: the,

entity: chairs-6 (plural)
  attributes: circle,
  count: 10
  relationships: in:circle-9,are on:outside-3,

entity: circle-9
  determiners: each,

Command count: 0
Done!
0
[[{'name': 'outside', 'index': '3', 'plural': 'n', 'determiners': 'the,'}, {'name': 'chairs', 'index': '6', 'plural': 'y', 'attributes': 'circle,', 'count': '10', 'relationships': 'in:circle-9,are on:outside-3,'}, {'name': 'circle', 'index': '9', 'plural': 'n', 'determiners': 'each,'}]]
[]
['', 'IN', 'DT', 'NN', 'VBP', 'CD', 'NNS', 'IN', 'DT', 'NN', '.']
[['case', ['outside-3', 'on-1']], ['det', ['outside-3', 'the-2']], ['nmod:on', ['are-4', 'outside-3']], ['root', ['root-0', 'are-4']], ['nummod', ['chairs-6', '10-5']], ['nsubj', ['are-4', 'chairs-6']], ['case', ['circle-9', 'in-7']], ['det', ['circle-9', 'each-8']], ['nmod:in', ['chairs-6', 'circle-9']], ['punct', ['are-4', '.-10']]]
[[{'name': 'outside', 'index': '3', 'plural': 'n', 'determiners': 'the,'}, {'name': 'chairs', 'index': '6', 'plural': 'y', 'attributes': 'circle,', 'count': '10', 'relationships': 'in:circle-9,are on:outside-3,'}, {'name': 'circle', 'index': '9', 'plural': 'n', 'determiners': 'each,'}]]
[]
['', 'IN', 'DT', 'NN', 'VBP', 'CD', 'NNS', 'IN', 'DT', 'NN', '.']
{}
outside-3
   attributes:
   determiners:the,
   relationships:

chairs-6
   attributes:circle,
   determiners:
   relationships:in:circle-9,are on:outside-3,
   count:10

circle-9
   attributes:
   determiners:each,
   relationships:

(-1, 1)
None
False
0
```

inside are 10 chairs in each circle.

```
advmod(chairs-4, inside-1~RB)
dep(chairs-4, are-2~VBP)
nummod(chairs-4, 10-3~CD)
root(root-0, chairs-4~NNS)
case(circle-7, in-5~IN)
det(circle-7, each-6~DT)
nmod:in(chairs-4, circle-7~NN)
punct(chairs-4, .-8~.)

Entity count: 2
entity: chairs-4 (plural)
  attributes: inside,circle,
  count: 10
  relationships: in:circle-7,

entity: circle-7
  determiners: each,

Command count: 0
Done!
0
[[{'name': 'chairs', 'index': '4', 'plural': 'y', 'attributes': 'inside,circle,', 'count': '10', 'relationships': 'in:circle-7,'}, {'name': 'circle', 'index': '7', 'plural': 'n', 'determiners': 'each,'}]]
[]
['', 'RB', 'VBP', 'CD', 'NNS', 'IN', 'DT', 'NN', '.']
[['advmod', ['chairs-4', 'inside-1']], ['dep', ['chairs-4', 'are-2']], ['nummod', ['chairs-4', '10-3']], ['root', ['root-0', 'chairs-4']], ['case', ['circle-7', 'in-5']], ['det', ['circle-7', 'each-6']], ['nmod:in', ['chairs-4', 'circle-7']], ['punct', ['chairs-4', '.-8']]]
[[{'name': 'chairs', 'index': '4', 'plural': 'y', 'attributes': 'inside,circle,', 'count': '10', 'relationships': 'in:circle-7,'}, {'name': 'circle', 'index': '7', 'plural': 'n', 'determiners': 'each,'}]]
[]
['', 'RB', 'VBP', 'CD', 'NNS', 'IN', 'DT', 'NN', '.']
{}
chairs-4
   attributes:inside,circle,
   determiners:
   relationships:in:circle-7,
   count:10

circle-7
   attributes:inside,
   determiners:each,
   relationships:

(1, -1)
circle-7
False
10
```





1. there are two circles of chairs in the outer circle, each with 10 chairs.
   expl(are-2, there-1~EX)
   root(root-0, are-2~VBP)
   nummod(circles-4, two-3~CD)
   nsubj(are-2, circles-4~NNS)
   case(chairs-6, of-5~IN)
   nmod:of(circles-4, chairs-6~NNS)
   case(circle-10, in-7~IN)
   det(circle-10, the-8~DT)
   amod(circle-10, outer-9~JJ)
   nmod:in(chairs-6, circle-10~NN)   (必须没有inner)
   punct(circle-10, ,-11~,)
   appos(circle-10, each-12~DT)
   case(chairs-15, with-13~IN)
   nummod(chairs-15, 10-14~CD)
   nmod:with(each-12, chairs-15~NNS)
   punct(are-2, .-16~.)

2. on the outside, there are 10 chairs in each circle.
   case(outside-3, on-1~IN)
   det(outside-3, the-2~DT)
   nmod:on(are-6, outside-3~JJ)
   punct(are-6, ,-4~,)
   expl(are-6, there-5~EX)
   root(root-0, are-6~VBP)
   nummod(chairs-8, 10-7~CD)
   nsubj(are-6, chairs-8~NNS)
   case(circle-11, in-9~IN)
   det(circle-11, each-10~DT)
   nmod:in(chairs-8, circle-11~NN)
   punct(are-6, .-12~.)

   chairs-6
      attributes:circle,
      determiners:
      **relationships:in:circle-9,are on:outside-3,**
      count:10

   circle-9
      attributes:
      **determiners:each,**
      relationships:

3. on the outside are 2 circles, each with 10 chairs.
   case(outside-3, on-1~IN)
   det(outside-3, the-2~DT)
   nmod:on(are-4, outside-3~NN)
   root(root-0, are-4~VBP)
   nummod(circles-6, 2-5~CD)
   nsubj(are-4, circles-6~NNS)
   punct(circles-6, ,-7~,)
   appos(circles-6, each-8~DT)
   case(chairs-11, with-9~IN)
   nummod(chairs-11, 10-10~CD)
   nmod:with(each-8, chairs-11~NNS)
   punct(are-4, .-12~.)

4. inside are 2 circles, each with 10 chairs.
   advmod(circles-4, inside-1~RB)
   dep(circles-4, are-2~VBP)
   nummod(circles-4, 2-3~CD)
   root(root-0, circles-4~NNS)
   punct(circles-4, ,-5~,)
   **appos(circles-4, each-6~DT)**
   case(chairs-9, with-7~IN)
   nummod(chairs-9, 10-8~CD)
   **nmod:with(each-6, chairs-9~NNS)**
   punct(circles-4, .-10~.)

5. each circle has 10 chairs.
   det(circle-2, each-1~DT)
   nsubj(has-3, circle-2~NN)
   root(root-0, has-3~VBZ)
   nummod(chairs-5, 10-4~CD)
   dobj(has-3, chairs-5~NNS)
   punct(has-3, .-6~.)

   entity: circle-2
     attributes: has,
     **determiners: each,**
     **relationships: has:chairs-5,**

   entity: chairs-5 (plural)
     count: 10





1. on the outside, there are 10 chairs in each circle. 为什么会把outside圈数判定成1？
2. 解决each with问题

each with: 

chair:

relationships: `each:circle-2`



1. ,each with 10 chairs
2. there are 10 chairs in each circle.
3. each circle has 10 chairs

