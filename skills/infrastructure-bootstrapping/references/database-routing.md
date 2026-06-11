# Database Routing Reference

关系数据库到迁移工具、Go 驱动、DDL 特征和连接配置的映射表。新增一种数据库时只需在此表加一行，不动 SKILL.md。

## 路由表

| 数据库 | 推荐迁移工具 | Go 驱动 | DDL 特征 | 开发容器镜像 | 默认端口 |
|--------|-------------|---------|----------|-------------|---------|
| **PostgreSQL** | Flyway | pgx (`github.com/jackc/pgx/v5`) | `SERIAL`/`BIGSERIAL` 自增, `JSONB`, `TIMESTAMPTZ`, `PARTITION BY RANGE`, 支持 CHECK CONSTRAINT | `postgres:16-alpine` | 5432 |
| **MySQL** | Flyway 或 golang-migrate | `github.com/go-sql-driver/mysql` | `AUTO_INCREMENT`, `JSON`, `DATETIME`/`TIMESTAMP`, `ENGINE=InnoDB`, `PARTITION BY RANGE` | `mysql:8.4` | 3306 |
| **SQLite** | golang-migrate 或 手动 SQL | `github.com/mattn/go-sqlite3` | `INTEGER PRIMARY KEY AUTOINCREMENT`, 无 JSONB(用 TEXT), 无分区 | (无需容器) | (文件) |
| **MongoDB** | (无需迁移，集合自动创建) | `go.mongodb.org/mongo-driver` | 无 DDL，以代码中的 struct tag 定义文档结构 | `mongo:7` | 27017 |
| **SQL Server** | Flyway (商业版) 或 DbUp | `github.com/denisenkom/go-mssqldb` | `IDENTITY(1,1)`, `NVARCHAR`, `DATETIME2`, `CREATE PARTITION FUNCTION` | `mcr.microsoft.com/mssql/server:2022-latest` | 1433 |

## 迁移工具判定规则

若设计文档未指定迁移工具，按以下优先级选择：

1. 若数据库是 PostgreSQL / MySQL / SQL Server 且 Flyway 为该生态主流 → **Flyway**
2. 若数据库是 SQLite → **golang-migrate**（Flyway 对 SQLite 支持弱）
3. 若数据库是 MongoDB → 跳过迁移工具（MongoDB 动态 schema）
4. 若项目 Java 为主 → 优先 **Flyway**（Java 生态标准）
5. 若项目 Go 为主 → **Flyway**（命令行可用）或 **golang-migrate**（Go 原生）

## Flyway 迁移文件

```
db/
├── migration/
│   └── V1__baseline.sql    ← 基线 DDL，版本号全局递增
└── model/                  ← 与 DDL 同步的实体代码（仅 Go，其他语言不需要）
```

**命名规则**：`V{版本号}__{描述}.sql`，双下划线。版本号全局递增，不回退。变更用补偿脚本 `V{N}__rollback_{描述}.sql`。

**V1__baseline.sql 内容来源**：从设计文档的数据设计章节直接提取建表语句。禁止自行发挥表结构。

## 开发环境 docker-compose 片段

### PostgreSQL
```yaml
db:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: <从设计文档读取或使用 dev>
    POSTGRES_PASSWORD: <从设计文档读取或使用 dev_pass>
    POSTGRES_DB: <从设计文档读取>
  ports:
    - "5433:5432"    # 避免与宿主机 PostgreSQL 冲突
  volumes:
    - pgdata:/var/lib/postgresql/data
```

### MySQL
```yaml
db:
  image: mysql:8.4
  environment:
    MYSQL_ROOT_PASSWORD: <密码>
    MYSQL_DATABASE: <数据库名>
  ports:
    - "3307:3306"    # 避免与宿主机 MySQL 冲突
  volumes:
    - mysqldata:/var/lib/mysql
```

### SQLite
不需要容器。在 `.gitignore` 中忽略 `.db` 文件。连接字符串直接指向文件路径。

### MongoDB
```yaml
db:
  image: mongo:7
  ports:
    - "27018:27017"
  volumes:
    - mongodata:/data/db
```
