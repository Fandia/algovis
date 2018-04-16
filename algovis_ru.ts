<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ru">
<context>
    <name>BFS</name>
    <message>
        <location filename="algorithms/graphs.py" line="204"/>
        <source>Breadth-first search</source>
        <translation>Поиск в ширину</translation>
    </message>
    <message>
        <location filename="algorithms/graphs.py" line="205"/>
        <source>
        &lt;b&gt;Breadth-first search&lt;/b&gt; (&lt;b&gt;BFS&lt;/b&gt;) is an algorithm for traversing or searching tree         or graph data structures. It starts at the tree root (or some arbitrary node         of a graph, sometimes referred to as a &apos;search key&apos;) and explores the neighbor         nodes first, before moving to the next level neighbours.
        BFS and its application in finding connected components of graphs were invented in         1945 by Michael Burke and Konrad Zuse, in his (rejected) Ph.D. thesis on the PlankalkÃ¼l         programming language, but this was not published until 1972. It was reinvented in 1959         by E. F. Moore, who used it to find the shortest path out of a maze, and discovered         independently by C. Y. Lee as a wire routing algorithm (published 1961).
        </source>
        <translation>Поиск в ширину работает путём последовательного просмотра отдельных уровней графа, начиная с узла-источника &lt;i&gt;u&lt;/i&gt;
Рассмотрим все рёбра &lt;i&gt;(u, v)&lt;/i&gt;, выходящие из узла &lt;i&gt;u&lt;/i&gt;. Если очередной узел &lt;i&gt;v&lt;/i&gt; является целевым узлом, то поиск завершается; в противном случае узел &lt;i&gt;v&lt;/i&gt; добавляется в очередь. После того, как будут проверены все рёбра, выходящие из узла &lt;i&gt;u&lt;/i&gt;, из очереди извлекается следующий узел &lt;i&gt;u&lt;/i&gt;, и процесс повторяется.</translation>
    </message>
</context>
<context>
    <name>BubbleSort</name>
    <message>
        <location filename="algorithms/sorting.py" line="127"/>
        <source>Bubble sort</source>
        <translation>Сортировка пузырьком</translation>
    </message>
    <message>
        <location filename="algorithms/sorting.py" line="128"/>
        <source>
        &lt;b&gt;Bubble sort&lt;/b&gt;, sometimes referred to as &lt;b&gt;sinking sort&lt;/b&gt;, is a simple sorting algorithm that repeatedly         steps through the list to be sorted, compares each pair of adjacent items and swaps them if they are         in the wrong order. The pass through the list is repeated until no swaps are needed, which indicates         that the list is sorted. The algorithm, which is a comparison sort, is named for the way smaller or         larger elements &quot;bubble&quot; to the top of the list. Although the algorithm is simple, it is too slow and         impractical for most problems even when compared to insertion sort. It can be practical if the input         is usually in sorted order but may occasionally have some out-of-order elements nearly in position.        </source>
        <translation>&lt;b&gt;Сортировка простыми обменами, сортиро́вка пузырько́м&lt;/b&gt; (англ. bubble sort) — простой алгоритм сортировки. Для понимания и реализации этот алгоритм — простейший, но эффективен он лишь для небольших массивов. Сложность алгоритма: &lt;b&gt;&lt;i&gt;O&lt;/i&gt;(&lt;i&gt;n&lt;/i&gt;&lt;sup&gt;2&lt;/sup&gt;)&lt;/b&gt;. Алгоритм считается учебным и практически не применяется вне учебной литературы, вместо него на практике применяются более эффективные алгоритмы сортировки. В то же время метод сортировки обменами лежит в основе некоторых более совершенных алгоритмов, таких как шейкерная сортировка, пирамидальная сортировка и быстрая сортировка.</translation>
    </message>
</context>
<context>
    <name>DFS</name>
    <message>
        <location filename="algorithms/graphs.py" line="250"/>
        <source>Depth-first search</source>
        <translation>Поиск в глубину</translation>
    </message>
    <message>
        <location filename="algorithms/graphs.py" line="251"/>
        <source>
        &lt;b&gt;Depth-first search&lt;/b&gt; (&lt;b&gt;DFS&lt;/b&gt;) is an algorithm for traversing or searching tree or graph data structures.         One starts at the root (selecting some arbitrary node as the root in the case of a graph) and explores         as far as possible along each branch before backtracking.
        A version of depth-first search was investigated in the 19th century by French mathematician         &lt;a href=&quot;https://en.wikipedia.org/wiki/Charles_Pierre_Tr%C3%A9maux&quot;&gt;Charles Pierre TrÃ©maux&lt;/a&gt; as a strategy for solving mazes.
        </source>
        <translation>&lt;b&gt;Поиск в глубину&lt;/b&gt; (англ. &lt;i&gt;Depth-first search&lt;/i&gt;, &lt;b&gt;DFS&lt;/b&gt;) — один из методов обхода графа. Стратегия поиска в глубину, как и следует из названия, состоит в том, чтобы идти «вглубь» графа, насколько это возможно. Алгоритм поиска описывается рекурсивно: перебираем все исходящие из рассматриваемой вершины рёбра. Если ребро ведёт в вершину, которая не была рассмотрена ранее, то запускаем алгоритм от этой нерассмотренной вершины, а после возвращаемся и продолжаем перебирать рёбра. Возврат происходит в том случае, если в рассматриваемой вершине не осталось рёбер, которые ведут в нерассмотренную вершину. Если после завершения алгоритма не все вершины были рассмотрены, то необходимо запустить алгоритм от одной из нерассмотренных вершин.</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="AlgoVis.py" line="16"/>
        <source>Algovis - algorithms visualization</source>
        <translation>Algovis - визуализация алгоритмов</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="20"/>
        <source>Sorting</source>
        <translation>Сортировка</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="32"/>
        <source>Minimum</source>
        <translation>Минимум</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="33"/>
        <source>Maximum</source>
        <translation>Максимум</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="34"/>
        <source>Elements count</source>
        <translation>Количество элементов</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="36"/>
        <source>Bubble sort</source>
        <translation>Сортировка пузырьком</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="38"/>
        <source>Quick sort</source>
        <translation>Быстрая сортировка</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="45"/>
        <source>Graphs</source>
        <translation>Графы</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="47"/>
        <source>Breadth-first search</source>
        <translation>Поиск в ширину</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="49"/>
        <source>Depth-first search</source>
        <translation>Поиск в глубину</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="61"/>
        <source>Width</source>
        <translation>Ширина сетки</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="62"/>
        <source>Height</source>
        <translation>Высота сетки</translation>
    </message>
    <message>
        <location filename="AlgoVis.py" line="63"/>
        <source>Nodes count</source>
        <translation>Количество узлов</translation>
    </message>
</context>
<context>
    <name>QuickSort</name>
    <message>
        <location filename="algorithms/sorting.py" line="166"/>
        <source>Quick sort</source>
        <translation>Быстрая сортировка</translation>
    </message>
    <message>
        <location filename="algorithms/sorting.py" line="167"/>
        <source>
        &lt;b&gt;Quicksort&lt;/b&gt; (sometimes called &lt;b&gt;partition-exchange sort&lt;/b&gt;) is an efficient sorting algorithm,         serving as a systematic method for placing the elements of an array in order.         Developed by &lt;a href=&quot;https://en.wikipedia.org/wiki/Tony_Hoare&quot;&gt;Tony Hoare&lt;/a&gt; in 1959 and published in 1961,         it is still a commonly used algorithm for sorting. When implemented well, it can be about two or three         times faster than its main competitors, merge sort and heapsort.
        Quicksort is a comparison sort, meaning that it can sort items of any type for which a &quot;less-than&quot; relation         (formally, a total order) is defined. In efficient implementations it is not a stable sort, meaning that the         relative order of equal sort items is not preserved. Quicksort can operate in-place on an array, requiring         small additional amounts of memory to perform the sorting. It is very similar to selection sort, except that         it does not always choose worst-case partition.
        </source>
        <translation>&lt;b&gt;Быстрая сортировка, сортировка Хоара&lt;/b&gt; (англ. quicksort), часто называемая &lt;b&gt;qsort&lt;/b&gt; (по имени в стандартной библиотеке языка Си) — широко известный алгоритм сортировки, разработанный английским информатиком &lt;a href=&quot;https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B0%D1%80,_%D0%A7%D0%B0%D1%80%D0%BB%D1%8C%D0%B7_%D0%AD%D0%BD%D1%82%D0%BE%D0%BD%D0%B8_%D0%A0%D0%B8%D1%87%D0%B0%D1%80%D0%B4&quot;&gt;Чарльзом Хоаром&lt;/a&gt; во время его работы в МГУ в 1960 году. Один из самых быстрых известных универсальных алгоритмов сортировки массивов: в среднем &lt;b&gt;&lt;i&gt;O&lt;/i&gt;(&lt;i&gt;n&lt;/i&gt;log&lt;i&gt;n&lt;/i&gt;)&lt;/b&gt; обменов при упорядочении &lt;i&gt;n&lt;/i&gt; элементов; из-за наличия ряда недостатков на практике обычно используется с некоторыми доработками.</translation>
    </message>
</context>
</TS>
