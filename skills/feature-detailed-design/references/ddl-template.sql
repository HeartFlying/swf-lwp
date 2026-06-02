-- ============================================
-- Feature 详细设计 - DDL 模板
-- ============================================
-- 使用说明：
-- 1. 替换 {entity_name} 为实际实体名（小写+下划线）
-- 2. 根据业务需求添加/删除字段
-- 3. 根据查询场景优化索引
-- 4. 大表（>1000万行）考虑分区策略
-- ============================================

-- --------------------------------------------
-- 1. 主业务表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS {entity_name}s (
    -- 主键（使用BIGINT或UUID）
    id BIGSERIAL PRIMARY KEY,

    -- 业务字段（根据Feature需求定义）
    -- 示例：名称、编码、状态等
    name VARCHAR(255) NOT NULL,
    code VARCHAR(64) UNIQUE,
    status VARCHAR(32) DEFAULT 'active',

    -- 外键（如有关联）
    -- related_id BIGINT REFERENCES other_table(id),

    -- 扩展字段（JSONB存储非结构化数据）
    metadata JSONB DEFAULT '{}',

    -- 时间戳（必须）
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- 软删除标记（可选）
    deleted_at TIMESTAMPTZ
);

-- 表注释
COMMENT ON TABLE {entity_name}s IS '{实体中文名}主表';
COMMENT ON COLUMN {entity_name}s.id IS '主键ID';
COMMENT ON COLUMN {entity_name}s.name IS '名称';
COMMENT ON COLUMN {entity_name}s.code IS '编码';
COMMENT ON COLUMN {entity_name}s.status IS '状态';
COMMENT ON COLUMN {entity_name}s.metadata IS '扩展字段';
COMMENT ON COLUMN {entity_name}s.created_at IS '创建时间';
COMMENT ON COLUMN {entity_name}s.updated_at IS '更新时间';

-- --------------------------------------------
-- 2. 关联表（多对多关系）
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS {entity_a}_{entity_b}_mapping (
    id BIGSERIAL PRIMARY KEY,
    {entity_a}_id BIGINT NOT NULL REFERENCES {entity_a}s(id) ON DELETE CASCADE,
    {entity_b}_id BIGINT NOT NULL REFERENCES {entity_b}s(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- 唯一约束（防止重复关联）
    UNIQUE({entity_a}_id, {entity_b}_id)
);

-- --------------------------------------------
-- 3. 索引设计（覆盖查询场景）
-- --------------------------------------------

-- 3.1 唯一索引
CREATE UNIQUE INDEX IF NOT EXISTS idx_{entity_name}_code
    ON {entity_name}s(code)
    WHERE deleted_at IS NULL;

-- 3.2 查询索引
CREATE INDEX IF NOT EXISTS idx_{entity_name}_status
    ON {entity_name}s(status);

-- 3.3 复合索引（常用组合查询）
CREATE INDEX IF NOT EXISTS idx_{entity_name}_status_created
    ON {entity_name}s(status, created_at DESC);

-- 3.4 JSONB索引（如需要按JSON字段查询）
CREATE INDEX IF NOT EXISTS idx_{entity_name}_metadata_gin
    ON {entity_name}s USING GIN(metadata);

-- --------------------------------------------
-- 4. 触发器（自动更新updated_at）
-- --------------------------------------------
CREATE OR REPLACE FUNCTION update_{entity_name}_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_{entity_name}_updated_at ON {entity_name}s;
CREATE TRIGGER trg_{entity_name}_updated_at
    BEFORE UPDATE ON {entity_name}s
    FOR EACH ROW
    EXECUTE FUNCTION update_{entity_name}_updated_at();

-- --------------------------------------------
-- 5. 分区表示例（大表使用）
-- --------------------------------------------
-- 适用于：轨迹点、日志、时序数据

-- 创建分区表（按时间范围分区）
CREATE TABLE IF NOT EXISTS {entity_name}_logs (
    id BIGSERIAL,
    {entity_name}_id BIGINT NOT NULL,
    log_data JSONB,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- 创建分区（每月一个分区）
CREATE TABLE IF NOT EXISTS {entity_name}_logs_y2024m01 PARTITION OF {entity_name}_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE IF NOT EXISTS {entity_name}_logs_y2024m02 PARTITION OF {entity_name}_logs
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- --------------------------------------------
-- 6. SQLite边缘缓存表（如需要）
-- --------------------------------------------
/*
CREATE TABLE IF NOT EXISTS edge_{entity_name}s (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id BIGINT,
    name TEXT NOT NULL,
    data BLOB,
    sync_status TEXT DEFAULT 'pending',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_edge_{entity_name}_sync
    ON edge_{entity_name}s(sync_status, created_at);
*/

-- --------------------------------------------
-- 7. 常用数据类型参考
-- --------------------------------------------
-- 字符串：VARCHAR(n) / TEXT
-- 整数：SMALLINT / INTEGER / BIGINT / SERIAL / BIGSERIAL
-- 浮点：REAL / DOUBLE PRECISION / NUMERIC(p,s)
-- 时间：DATE / TIME / TIMESTAMPTZ
-- JSON：JSONB (PostgreSQL) / TEXT (SQLite)
-- 布尔：BOOLEAN / INTEGER (SQLite)
-- 二进制：BYTEA (PostgreSQL) / BLOB (SQLite)

-- --------------------------------------------
-- 8. 权限控制（可选）
-- --------------------------------------------
-- GRANT SELECT, INSERT, UPDATE ON {entity_name}s TO app_user;
-- GRANT ALL ON {entity_name}s TO admin_user;
