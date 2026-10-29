# 2048

## 运行

需要 Python 3：

```bash
python3 game2048.py
```

使用 `W/A/S/D` 移动，输入 `Q` 退出。

## 教学用安全缺陷

游戏把最高分写入程序目录下的 `highscore.json`，并在启动时直接信任其中的 `high_score`。可以在玩出分数并生成该文件后，手动把分数改大；重新启动后，游戏会显示伪造的最高分。这是本地数据完整性缺陷，仅用于演示，不涉及网络访问或代码执行。

## CodeQL 跨文件数据流样例

`codeql-demo/` 提供一个与游戏隔离的 CodeQL 自定义查询样例。查询把固定字符串视为合成 source，追踪它经过 `pipeline.py` 和 `transform.py`，到达 `sink.py` 中仅向内存列表追加数据的 sink。样例不读取用户输入，也不访问文件、网络或执行命令；不会被游戏导入或运行。

安装 CodeQL CLI 后，可从仓库根目录创建仅包含样例的 Python 数据库并运行查询：

```bash
codeql pack install codeql-demo
codeql database create /tmp/game-codeql-fixture-db \
  --language=python \
  --source-root=codeql-demo/fixture
codeql database analyze /tmp/game-codeql-fixture-db codeql-demo \
  --format=sarif-latest \
  --output=/tmp/game-codeql-fixture.sarif
```

预期 SARIF 中有一条结果，位置在 `sink.py` 的 `fixture_sink(build_value())` 调用处。查询使用全局污点追踪，因此该结果验证 source 到 sink 的跨函数、跨文件传播；它是自定义检测样例，不代表 CodeQL 内置规则会报告此模式。
