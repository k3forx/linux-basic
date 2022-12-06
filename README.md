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
