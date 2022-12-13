# linux-basic

## 静的ライブラリと共有ライブラリ

静的はコンパイルときにバイナリに組み込まれる、共有ライブラリは実行時にメモリにロードされる

- システム全体としてサイズを小さく抑えられる

## プロセス管理 (基礎編)

```bash
root@e33ed6ff431f:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4624  3752 pts/0    Ss+  14:10   0:00 bash
root        17  0.0  0.0   4624  3880 pts/1    Ss   14:11   0:00 bash
root        28  0.0  0.0   7060  1556 pts/1    R+   14:12   0:00 ps aux
root@e33ed6ff431f:/#
```

新しくプロセスを生成する目的

- 同じプログラムの処理を複数のプロセスに分けて処理する
- 別のプログラムを生成する

### 別のプログラムを起動する `execve()` 関数

`fork()` 関数によってプロセスのコピーを作った後は、子プロセス上で `execve()` 関数を発行する。これによって子プロセスは、別のプログラムに置き換えられる。

1. `execve()` 関数を呼び出す
1. `execve()` 関数の引数で指定した実行ファイルからプログラムを読み出して、メモリ上に配置する (メモリマップ) ために必要な情報を読み出す
1. 現在のプロセスのメモリを新しいプロセスのデータで上書きする
1. プロセスを新しいプロセスの最初に実行すべき命令 (エントリポイント) から実行開始する

`exec()` 関数の実現のために、実行ファイルはプログラムのコードやデータに加えて、次のようなプログラムの起動に必要なデータを保持している。

- コード領域のファイル上オフセット、サイズ、およびメモリマップ開始アドレス
- データ領域についての上記と同じ情報
- 最初に実行する命令のメモリアドレス (エントリポイント)

```bash
root@860fc4e32cd0:/home/src/process_management_basic# cc -o pause -no-pie pause.c
root@860fc4e32cd0:/home/src/process_management_basic# readelf -h pause
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2 seconds complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x401050 // 開始アドレス
  Start of program headers:          64 (bytes into file)
  Start of section headers:          13912 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         13
  Size of section headers:           64 (bytes)
  Number of section headers:         31
  Section header string table index: 30
root@860fc4e32cd0:/home/src/process_management_basic# readelf -S pause
There are 31 section headers, starting at offset 0x3658:

Section Headers:
  [Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [ 1] .interp           PROGBITS         0000000000400318  00000318
       000000000000001c  0000000000000000   A       0     0     1
  [ 2] .note.gnu.pr[...] NOTE             0000000000400338  00000338
       0000000000000030  0000000000000000   A       0     0     8
  [ 3] .note.gnu.bu[...] NOTE             0000000000400368  00000368
       0000000000000024  0000000000000000   A       0     0     4
  [ 4] .note.ABI-tag     NOTE             000000000040038c  0000038c
       0000000000000020  0000000000000000   A       0     0     4
  [ 5] .gnu.hash         GNU_HASH         00000000004003b0  000003b0
       000000000000001c  0000000000000000   A       6     0     8
  [ 6] .dynsym           DYNSYM           00000000004003d0  000003d0
       0000000000000060  0000000000000018   A       7     1     8
  [ 7] .dynstr           STRTAB           0000000000400430  00000430
       0000000000000049  0000000000000000   A       0     0     1
  [ 8] .gnu.version      VERSYM           000000000040047a  0000047a
       0000000000000008  0000000000000002   A       6     0     2
  [ 9] .gnu.version_r    VERNEED          0000000000400488  00000488
       0000000000000030  0000000000000000   A       7     1     8
  [10] .rela.dyn         RELA             00000000004004b8  000004b8
       0000000000000030  0000000000000018   A       6     0     8
  [11] .rela.plt         RELA             00000000004004e8  000004e8
       0000000000000018  0000000000000018  AI       6    24     8
  [12] .init             PROGBITS         0000000000401000  00001000
       000000000000001b  0000000000000000  AX       0     0     4
  [13] .plt              PROGBITS         0000000000401020  00001020
       0000000000000020  0000000000000010  AX       0     0     16
  [14] .plt.sec          PROGBITS         0000000000401040  00001040
       0000000000000010  0000000000000010  AX       0     0     16
  [15] .text             PROGBITS         0000000000401050  00001050
       00000000000000fa  0000000000000000  AX       0     0     16
  [16] .fini             PROGBITS         000000000040114c  0000114c
       000000000000000d  0000000000000000  AX       0     0     4
  [17] .rodata           PROGBITS         0000000000402000  00002000
       0000000000000004  0000000000000004  AM       0     0     4
  [18] .eh_frame_hdr     PROGBITS         0000000000402004  00002004
       0000000000000034  0000000000000000   A       0     0     4
  [19] .eh_frame         PROGBITS         0000000000402038  00002038
       00000000000000a4  0000000000000000   A       0     0     8
  [20] .init_array       INIT_ARRAY       0000000000403e10  00002e10
       0000000000000008  0000000000000008  WA       0     0     8
  [21] .fini_array       FINI_ARRAY       0000000000403e18  00002e18
       0000000000000008  0000000000000008  WA       0     0     8
  [22] .dynamic          DYNAMIC          0000000000403e20  00002e20
       00000000000001d0  0000000000000010  WA       7     0     8
  [23] .got              PROGBITS         0000000000403ff0  00002ff0
       0000000000000010  0000000000000008  WA       0     0     8
  [24] .got.plt          PROGBITS         0000000000404000  00003000
       0000000000000020  0000000000000008  WA       0     0     8
  [25] .data             PROGBITS         0000000000404020  00003020
       0000000000000010  0000000000000000  WA       0     0     8
  [26] .bss              NOBITS           0000000000404030  00003030
       0000000000000008  0000000000000000  WA       0     0     1
  [27] .comment          PROGBITS         0000000000000000  00003030
       000000000000002b  0000000000000001  MS       0     0     1
  [28] .symtab           SYMTAB           0000000000000000  00003060
       0000000000000330  0000000000000018          29    18     8
  [29] .strtab           STRTAB           0000000000000000  00003390
       00000000000001a2  0000000000000000           0     0     1
  [30] .shstrtab         STRTAB           0000000000000000  00003532
       000000000000011f  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  D (mbind), l (large), p (processor specific)

```

pause プログラムを実行するのに必要な情報

| 名前                                              | 値       |
| ------------------------------------------------- | -------- |
| コードのファイル内オフセット (.text, Offset)      | 0x1050   |
| コードのサイズ (.text, Size)                      | 0xfa     |
| コードのメモリマップ開始アドレス (.text, Address) | 0x401050 |
| データのファイル内オフセット (.data, Offset)      | 0x3020   |
| データのサイズ (.data, Size)                      | 0x10     |
| データのメモリマップ開始アドレス (.data, Address) | 0x404020 |
| エントリポイント                                  | 0x401050 |

メモリマップ

```bash
root@860fc4e32cd0:/home/src/process_management_basic# ./pause &
[1] 29
root@860fc4e32cd0:/home/src/process_management_basic# cat /proc/29/maps
00400000-00401000 r--p 00000000 00:78 46645260                           /home/src/process_management_basic/pause
00401000-00402000 r-xp 00001000 00:78 46645260                           /home/src/process_management_basic/pause
00402000-00403000 r--p 00002000 00:78 46645260                           /home/src/process_management_basic/pause
00403000-00404000 r--p 00002000 00:78 46645260                           /home/src/process_management_basic/pause
00404000-00405000 rw-p 00003000 00:78 46645260                           /home/src/process_management_basic/pause
7f5a7ec7b000-7f5a7ec7e000 rw-p 00000000 00:00 0
7f5a7ec7e000-7f5a7eca6000 r--p 00000000 fe:01 2104506                    /usr/lib/x86_64-linux-gnu/libc.so.6
7f5a7eca6000-7f5a7ee3b000 r-xp 00028000 fe:01 2104506                    /usr/lib/x86_64-linux-gnu/libc.so.6
7f5a7ee3b000-7f5a7ee93000 r--p 001bd000 fe:01 2104506                    /usr/lib/x86_64-linux-gnu/libc.so.6
7f5a7ee93000-7f5a7ee97000 r--p 00214000 fe:01 2104506                    /usr/lib/x86_64-linux-gnu/libc.so.6
7f5a7ee97000-7f5a7ee99000 rw-p 00218000 fe:01 2104506                    /usr/lib/x86_64-linux-gnu/libc.so.6
7f5a7ee99000-7f5a7eea6000 rw-p 00000000 00:00 0
7f5a7eea9000-7f5a7eeab000 rw-p 00000000 00:00 0
7f5a7eeab000-7f5a7eead000 r--p 00000000 fe:01 2104488                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
7f5a7eead000-7f5a7eed7000 r-xp 00002000 fe:01 2104488                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
7f5a7eed7000-7f5a7eee2000 r--p 0002c000 fe:01 2104488                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
7f5a7eee3000-7f5a7eee5000 r--p 00037000 fe:01 2104488                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
7f5a7eee5000-7f5a7eee7000 rw-p 00039000 fe:01 2104488                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
7ffeb08d8000-7ffeb08f9000 rw-p 00000000 00:00 0                          [stack]
7ffeb09dd000-7ffeb09e1000 r--p 00000000 00:00 0                          [vvar]
7ffeb09e1000-7ffeb09e3000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
```

### プロセスの親子関係

プロセスの親子関係

```bash
root@8314006d192b:/# pstree -p
bash(1)
```

### プロセスの状態

START: プロセスが起動した時間
TIME: 使った CPU 時間の合計
STAT: 一文字目が S のプロセスはスリープ状態

```bash
root@8314006d192b:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4624  3660 pts/0    Ss+  13:19   0:00 bash
root         9  0.0  0.0   4624  3716 pts/1    Ss   13:20   0:00 bash
root        22  0.0  0.0   7060  1548 pts/1    R+   13:21   0:00 ps aux
```

プロセスが CPU を使いたい状態 -> 実行可能状態
プロセスが CPU を使っている状態 -> 実行状態
プロセスが終了している状態 -> ゾンビ状態

### プロセスの終了

- プロセスを終了させるには exit_group()というシステムコールを呼ぶ
- exit_group()関数の中で、カーネルはメモリなどのプロセスのリソースを回収する

### シグナル

- シグナルとは、あるプロセスが他のプロセスに何かを通知して、外部から実行の流れを強制的に変えるための仕組み
- プロセスは各シグナルについて、シグナルハンドラという処理をあらかじめ登録しておける

シグナルハンドラで無視するコード

```python
#!/usr/bin/python3

import signal

signal.signal(signal.SIGINT, signal.SIG_IGN)

while True:
	pass
```

### シェルのジョブ管理の実現

- ジョブはシェルがバックグラウンドで実行したプロセスを制御するための仕組み

```bash
root@8314006d192b:/home/src/process_management_basic# sleep infinity &
[1] 37 # [1]がジョブの番号
root@8314006d192b:/home/src/process_management_basic# sleep infinity &
[2] 38
root@8314006d192b:/home/src/process_management_basic# jobs
[1]-  Running                 sleep infinity &
[2]+  Running                 sleep infinity &
root@8314006d192b:/home/src/process_management_basic# fg 1
sleep infinity
^Z
[1]+  Stopped                 sleep infinity
```

- セッションはユーザがシステムにログインした時のログインセッションに対応するもの
- セッションにはセッション ID、SID と呼ばれる一意な値が割り振られている
- TTY というフィールドが端末の名前

```bash
root@8314006d192b:/home/src/process_management_basic# ps ajx
 PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND
    0     1     1     1 pts/0        1 Ss+      0   0:00 bash
    0     9     9     9 pts/1       43 Ss       0   0:00 bash
    9    43    43     9 pts/1       43 R+       0   0:00 ps ajx
```

- プロセスグループは、複数のプロセスをまとめたコントロールするためのもの
- セッションの中に複数のプロセスグループが存在する

### デーモン

## プロセススケジューラ

- プロセスへの CPU リソースの割り当てを担当する Linux カーネルの機能をプロセススケジューラ (スケジューラ) という
- スケジューラの説明
  - 1 つの論理 CPU 上で同時に動けるプロセスは 1 つだけ
  - 実行可能な複数のプロセスに、タイムスライスと呼ばれる単位で順番に CPU を使わせる

### 経過時間と使用時間

- 経過時間: プロセスが開始してから終了するまでの経過時間
- 使用時間: プロセスが実際に論理 CPU を使用した時間

実験

```python
#!/usr/bin/python3

NLOOP = 100000000

for _ in range(NLOOP):
	pass
```

結果

- real は経過時間
- user と sys は使用時間
  - user はプロセスがユーザーランドで動作していた時間
  - sys はプロセスによるシステムコール発行の延長、カーネルが動作していた時の時間
- 1 つの CPU 上で動けるの 1 つのプロセスのみ

```bash
root@8314006d192b:/home/src/scheduler# time ./load.py

real    0m3.528s
user    0m3.517s
sys     0m0.004s
```

### タイムスライス

- スケジューラが実行可能プロセスにタイムスライス単位で CPU を使わせることを確かめる
- 各プロセスのタイムスライスは kernel.sched_latency_ns / <論理 CPU 上で実行中また実行可能状態のプロセス数> [ナノ秒] になる
- kernel.sched_latency_ns はレイテンシーターゲットと呼ばれる
- レイテンシターゲットやタイムスライスの値の計算は、プロセスの数が増えてきた場合やマルチコア CPU の場合はもう少し複雑になる

### コンテキストスイッチ

- 論理 CPU 上で動作するプロセスが切り替わることをコンテキストスイッチと呼ぶ
- コンテキストスイッチは、プロセスがいかなるコードを実行中でもタイムスライスが切れると容赦無く発生する

## メモリ管理システム

### メモリ関連情報の取得

`free` コマンドで

- システムが搭載するメモリの量
- 使用中のメモリの量

がわかる

```bash
root@8314006d192b:/home/src/scheduler# free
               total        used        free      shared  buff/cache   available
Mem:         8047196      312876     6517908      342640     1216412     7133632
Swap:        1048572           0     1048572
```

- total: システムに搭載されている全メモリの量
- free: 見かけ上の空きメモリ
- buff/cache: バッファキャッシュ、およびページキャッシュが使用するメモリ。システムの空きメモリ (free フィールド) が減少してきたら、カーネルによって解放される
- available: 実質的な空きメモリ。free フィールドの値に、空きメモリが足りなくなってきたら解放できるカーネル内のメモリ領域
- used: システムあ使用中のメモリから buff/cache を引いたもの

### 仮想記憶

#### 仮想記憶がない時の課題

以下のような課題が生じる。

- メモリの断片化
  - メモリの獲得、解放を繰り返すと、メモリの断片化という問題が発生する。
- マルチプロセスの実現が困難
  - あるプログラム A と B があり、それぞれが同じメモリ領域にマップされていることを期待している場合、A と B を同時に動かせない。
- 不正な領域へのアクセス
  - あるプロセスがカーネルや他のプロセスに割り当てられたメモリのアドレスを指定すれば、それらの領域にアクセスできてしまう。

#### 仮想記憶の機能

- 仮想記憶は、プロセスがメモリアクセスする際に、システムに搭載されているメモリに直接アクセスさせるのではなく、仮想アドレスというアドレスを用いて、間接的にアクセスさせるという機能
- 仮想アドレスから物理アドレスへの変換には、カーネルのメモリ内に保存されている「ページテーブル」という表を用いる。
- アドレス空間にはないアドレスにアクセスしようとすると、CPU 上でページフォールトという例外が発生する。

### プロセスへの新規メモリの割り当て

- メモリ領域の割り当て: 仮想アドレス空間に新規にアクセス可能なメモリ領域をマップする。
  - `mmap()` システムコールを使用する
- メモリの割り当て: 上記メモリ領域に物理メモリを割り当てる。
  - `mmap()` システムコールの呼び出し直後、新規メモリ領域に対応する物理メモリはまだ存在しない。新規領域の中の各ページに最初にアクセスした時に物理メモリを割り当てる。これはデマンドページングと呼ばれる。
  - 該当ページにアクセスすると以下のようにメモリを確保する
    1. プロセスがページにアクセス
    1. ページフォールト発生
    1. カーネルのページフォールトハンドラが動作して、ページに対応する物理メモリを割り当てる
