mathdoku-solver
===============

MathDoku/CalcuDoku/KenKen/KenDoku arithmetic puzzle solver.

The solver reads the following input format from text file or string:
<pre>
n m
x_0_0 x_0_1 ... x_0_n-1
x_1_0 x_1_1 ... x_1_n-1
...
x_n-1_0 x_n-1_1 ... x_n-1_n-1
0 op_0 v_0
1 op_1 v_1
...
m-1 op_m-1 v_m-1
</pre>

Where:
<table>
<tr>
	<td>n</td>
	<td>Size of MathDoku grid length.</td>
<tr>
	<td>m</td>
	<td>Number of cages.</td>
<tr>
	<td>x_(i)_(j)</td>
	<td>
		Cage index in the grid layout at row (i) and column (j).<br />
		Index starts with 0.
	</td>
<tr>
	<td>op_(i)</td>
	<td>
		Arithmetical operation to perform on the cage at index (i).<br />
		Valid operations are:
		<ul>
			<li>Addition (+)
			<li>Subtraction (-)
			<li>Multiplication (*)
			<li>Division (/)
		</ul>
	</td>
<tr>
	<td>v_(i)</td>
	<td>Value of the arithmetical operation on all cell values in the cage.</td>
</table>

Sample 4x4 MathDoku problem with 6 cages:
<pre>
4 6
0 0 0 1
2 2 3 1
4 2 1 1
4 2 5 5
0 * 24
1 + 10
2 * 24
3 + 3
4 - 1
5 / 4
</pre>

Sample solution for the problem above:
<pre>
=========
|3 4 2 1|
|4 1 3 2|
|1 2 4 3|
|2 3 1 4|
=========
</pre>
