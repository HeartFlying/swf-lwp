# Feature 详细设计 - 代码骨架模板

## 目录

1. [后端代码骨架](#后端代码骨架)
   - [Go](#go)
   - [FastAPI (Python)](#fastapi-python)
   - [Spring Boot (Java)](#spring-boot-java)
2. [算法侧代码骨架](#算法侧代码骨架)
   - [C++17](#c17)
3. [前端代码骨架](#前端代码骨架)
   - [Vue3 + TypeScript](#vue3--typescript)
4. [代码规范说明](#代码规范说明)

---

## 后端代码骨架

### Go

#### 目录结构

```
{feature}/
├── handler/
│   └── {entity}_handler.go    # HTTP Handler
├── service/
│   └── {entity}_service.go    # 业务逻辑层
├── repository/
│   └── {entity}_repo.go       # 数据访问层
├── model/
│   └── {entity}.go            # 领域模型 + DTO
└── router/
    └── router.go              # 路由注册
```

#### model/{entity}.go

```go
package model

import "time"

// {Entity} 领域实体
type {Entity} struct {
	ID        int64      `json:"id"         db:"id"`
	Name      string     `json:"name"       db:"name"`
	Code      *string    `json:"code"       db:"code"`
	Status    string     `json:"status"     db:"status"`
	Metadata  []byte     `json:"metadata"   db:"metadata"`
	CreatedAt time.Time  `json:"createdAt"  db:"created_at"`
	UpdatedAt time.Time  `json:"updatedAt"  db:"updated_at"`
	DeletedAt *time.Time `json:"-"          db:"deleted_at"`
}

// Create{Entity}Request 创建请求
type Create{Entity}Request struct {
	Name    string  `json:"name"    validate:"required,max=255"`
	Code    *string `json:"code"    validate:"omitempty,max=64"`
	Status  string  `json:"status"`
}

// Update{Entity}Request 更新请求
type Update{Entity}Request struct {
	Name   *string `json:"name"    validate:"omitempty,max=255"`
	Status *string `json:"status"`
}

// {Entity}ListResponse 列表响应
type {Entity}ListResponse struct {
	Items    []{Entity} `json:"items"`
	Total    int64      `json:"total"`
	Page     int        `json:"page"`
	PageSize int        `json:"pageSize"`
}
```

#### repository/{entity}_repo.go

```go
package repository

import (
	"context"
	"database/sql"

	"{module}/internal/model"
)

// {Entity}Repository 数据访问层
type {Entity}Repository struct {
	db *sql.DB
}

func New{Entity}Repository(db *sql.DB) *{Entity}Repository {
	return &{Entity}Repository{db: db}
}

// Create 插入记录
func (r *{Entity}Repository) Create(ctx context.Context, m *model.{Entity}) error {
	const query = `
		INSERT INTO {entity}s (name, code, status, metadata)
		VALUES ($1, $2, $3, $4)
		RETURNING id, created_at, updated_at`
	return r.db.QueryRowContext(ctx, query,
		m.Name, m.Code, m.Status, m.Metadata,
	).Scan(&m.ID, &m.CreatedAt, &m.UpdatedAt)
}

// GetByID 按主键查询
func (r *{Entity}Repository) GetByID(ctx context.Context, id int64) (*model.{Entity}, error) {
	const query = `
		SELECT id, name, code, status, metadata, created_at, updated_at
		FROM {entity}s
		WHERE id = $1 AND deleted_at IS NULL`
	m := &model.{Entity}{}
	err := r.db.QueryRowContext(ctx, query, id).Scan(
		&m.ID, &m.Name, &m.Code, &m.Status, &m.Metadata,
		&m.CreatedAt, &m.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return m, nil
}

// List 分页查询
func (r *{Entity}Repository) List(ctx context.Context, params model.ListParams) (*model.{Entity}ListResponse, error) {
	// 构建动态查询；实际实现中应使用查询构造器
	const countQuery = `SELECT COUNT(*) FROM {entity}s WHERE deleted_at IS NULL`
	const dataQuery = `
		SELECT id, name, code, status, metadata, created_at, updated_at
		FROM {entity}s
		WHERE deleted_at IS NULL
		ORDER BY created_at DESC
		LIMIT $1 OFFSET $2`

	var total int64
	if err := r.db.QueryRowContext(ctx, countQuery).Scan(&total); err != nil {
		return nil, err
	}

	rows, err := r.db.QueryContext(ctx, dataQuery, params.PageSize, (params.Page-1)*params.PageSize)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var items []model.{Entity}
	for rows.Next() {
		var m model.{Entity}
		if err := rows.Scan(&m.ID, &m.Name, &m.Code, &m.Status, &m.Metadata, &m.CreatedAt, &m.UpdatedAt); err != nil {
			return nil, err
		}
		items = append(items, m)
	}

	return &model.{Entity}ListResponse{
		Items:    items,
		Total:    total,
		Page:     params.Page,
		PageSize: params.PageSize,
	}, nil
}
```

#### service/{entity}_service.go

```go
package service

import (
	"context"
	"database/sql"
	"errors"
	"fmt"

	"{module}/internal/model"
	"{module}/internal/repository"
)

// 领域错误定义
var (
	Err{Entity}NotFound  = errors.New("实体不存在")
	Err{Entity}CodeDup   = errors.New("编码已存在")
)

// {Entity}Service 业务逻辑层
type {Entity}Service struct {
	repo *repository.{Entity}Repository
}

func New{Entity}Service(repo *repository.{Entity}Repository) *{Entity}Service {
	return &{Entity}Service{repo: repo}
}

// Create 创建实体
// 消费上游组件设计中的 [状态机锚点: {Entity}StateMachine.initial]
func (s *{Entity}Service) Create(ctx context.Context, req model.Create{Entity}Request) (*model.{Entity}, error) {
	m := &model.{Entity}{
		Name:   req.Name,
		Code:   req.Code,
		Status: "active",
	}
	if err := s.repo.Create(ctx, m); err != nil {
		return nil, fmt.Errorf("创建{实体}失败: %w", err)
	}
	return m, nil
}

// GetByID 按ID查询
func (s *{Entity}Service) GetByID(ctx context.Context, id int64) (*model.{Entity}, error) {
	m, err := s.repo.GetByID(ctx, id)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, Err{Entity}NotFound
	}
	return m, err
}

// List 分页列表查询
func (s *{Entity}Service) List(ctx context.Context, params model.ListParams) (*model.{Entity}ListResponse, error) {
	return s.repo.List(ctx, params)
}

// Update 更新实体
// 消费上游组件设计中的 [状态机锚点: {Entity}StateMachine.transition]
func (s *{Entity}Service) Update(ctx context.Context, id int64, req model.Update{Entity}Request) (*model.{Entity}, error) {
	// 算法锚点: 参考上游组件设计 [算法: {Entity}Validation]
	m, err := s.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}
	// 状态迁移校验 (上游状态机定义)
	if req.Status != nil && !isValidTransition(m.Status, *req.Status) {
		return nil, fmt.Errorf("非法状态迁移: %s -> %s", m.Status, *req.Status)
	}
	return m, nil
}

// Delete 软删除
func (s *{Entity}Service) Delete(ctx context.Context, id int64) error {
	// 异常处理锚点: 参考上游组件设计 [异常: {Entity}.Delete.NotFound]
	return nil
}
```

#### handler/{entity}_handler.go

```go
package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"{module}/internal/model"
	"{module}/internal/service"
)

// {Entity}Handler HTTP 处理层
type {Entity}Handler struct {
	svc *service.{Entity}Service
}

func New{Entity}Handler(svc *service.{Entity}Service) *{Entity}Handler {
	return &{Entity}Handler{svc: svc}
}

// HandleList GET /api/v1/{features}
func (h *{Entity}Handler) HandleList(w http.ResponseWriter, r *http.Request) {
	params := model.ListParams{
		Page:     queryInt(r, "page", 1),
		PageSize: queryInt(r, "pageSize", 20),
	}
	result, err := h.svc.List(r.Context(), params)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "INTERNAL_ERROR", err.Error())
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"data": result})
}

// HandleCreate POST /api/v1/{features}
func (h *{Entity}Handler) HandleCreate(w http.ResponseWriter, r *http.Request) {
	var req model.Create{Entity}Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "BAD_REQUEST", "请求格式错误")
		return
	}
	result, err := h.svc.Create(r.Context(), req)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "CREATE_FAILED", err.Error())
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"data": result})
}

// HandleGetByID GET /api/v1/{features}/{id}
func (h *{Entity}Handler) HandleGetByID(w http.ResponseWriter, r *http.Request) {
	id, err := pathID(r)
	if err != nil {
		writeError(w, http.StatusBadRequest, "BAD_REQUEST", "无效ID")
		return
	}
	result, err := h.svc.GetByID(r.Context(), id)
	if errors.Is(err, service.Err{Entity}NotFound) {
		writeError(w, http.StatusNotFound, "NOT_FOUND", err.Error())
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"data": result})
}
```

---

### FastAPI (Python)

#### 目录结构

```
{feature}/
├── __init__.py
├── main.py                 # FastAPI 入口
├── config.py               # 配置管理
├── models/
│   ├── __init__.py
│   ├── schemas.py          # Pydantic 模型
│   └── database.py         # SQLAlchemy 模型
├── services/
│   ├── __init__.py
│   └── {entity}_service.py # 业务服务
├── api/
│   ├── __init__.py
│   └── routes.py           # API 路由
└── core/
    ├── __init__.py
    ├── exceptions.py       # 异常定义
    └── security.py         # 认证授权
```

#### models/schemas.py

```python
"""Pydantic 数据模型"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class {Entity}Base(BaseModel):
    """基础字段"""
    name: str = Field(..., max_length=255, description="名称")
    code: Optional[str] = Field(None, max_length=64, description="编码")
    status: str = Field("active", description="状态")
    metadata: Optional[dict] = Field({}, description="扩展字段")


class {Entity}Create({Entity}Base):
    """创建请求"""
    pass


class {Entity}Update(BaseModel):
    """更新请求（所有字段可选）"""
    name: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None)
    metadata: Optional[dict] = Field(None)


class {Entity}Response({Entity}Base):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class {Entity}ListResponse(BaseModel):
    """列表响应"""
    items: list[{Entity}Response]
    total: int
    page: int
    page_size: int
```

#### services/{entity}_service.py

```python
"""业务服务层"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from ..models.database import {Entity}
from ..models.schemas import {Entity}Create, {Entity}Update, {Entity}ListResponse
from ..core.exceptions import NotFoundException, ConflictException


class {Entity}Service:
    """{实体} 业务服务"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: {Entity}Create) -> {Entity}:
        """创建实体"""
        # 检查编码是否重复
        if data.code and self._check_code_exists(data.code):
            raise ConflictException(f"编码已存在: {data.code}")

        entity = {Entity}(**data.model_dump())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, id: int) -> {Entity}:
        """根据ID查询"""
        entity = self.db.query({Entity}).filter(
            {Entity}.id == id,
            {Entity}.deleted_at.is_(None)
        ).first()

        if not entity:
            raise NotFoundException(f"实体不存在: {id}")

        return entity

    def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> {Entity}ListResponse:
        """分页查询列表"""
        query = self.db.query({Entity}).filter({Entity}.deleted_at.is_(None))

        # 过滤条件
        if status:
            query = query.filter({Entity}.status == status)
        if keyword:
            query = query.filter({Entity}.name.ilike(f"%{keyword}%"))

        # 排序
        sort_column = getattr({Entity}, sort_by, {Entity}.created_at)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # 分页
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        return {Entity}ListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )

    def update(self, id: int, data: {Entity}Update) -> {Entity}:
        """更新实体"""
        entity = self.get_by_id(id)

        # 只更新非空字段
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(entity, key, value)

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, id: int) -> None:
        """软删除实体"""
        entity = self.get_by_id(id)
        entity.deleted_at = datetime.now()
        self.db.commit()

    def _check_code_exists(self, code: str) -> bool:
        """检查编码是否已存在"""
        return self.db.query({Entity}).filter(
            {Entity}.code == code,
            {Entity}.deleted_at.is_(None)
        ).first() is not None
```

#### api/routes.py

```python
"""API 路由"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..models.schemas import (
    {Entity}Create, {Entity}Update, {Entity}Response,
    {Entity}ListResponse, BaseResponse
)
from ..services.{entity}_service import {Entity}Service
from ..core.database import get_db
from ..core.security import get_current_user

router = APIRouter(prefix="/{features}", tags=["{Feature}"])


def get_service(db: Session = Depends(get_db)) -> {Entity}Service:
    """依赖注入：获取服务实例"""
    return {Entity}Service(db)


@router.get(
    "",
    response_model=BaseResponse[{Entity}ListResponse],
    summary="查询列表"
)
async def list_{features}(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态过滤"),
    keyword: Optional[str] = Query(None, description="关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    service: {Entity}Service = Depends(get_service),
    current_user = Depends(get_current_user)
):
    """分页查询 {实体} 列表"""
    result = service.get_list(
        page=page,
        page_size=page_size,
        status=status,
        keyword=keyword,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return BaseResponse(data=result)


@router.post(
    "",
    response_model=BaseResponse[{Entity}Response],
    status_code=status.HTTP_201_CREATED,
    summary="创建"
)
async def create_{entity}(
    data: {Entity}Create,
    service: {Entity}Service = Depends(get_service),
    current_user = Depends(get_current_user)
):
    """创建新的 {实体}"""
    result = service.create(data)
    return BaseResponse(data=result)


@router.get(
    "/{id}",
    response_model=BaseResponse[{Entity}Response],
    summary="查询详情"
)
async def get_{entity}(
    id: int,
    service: {Entity}Service = Depends(get_service),
    current_user = Depends(get_current_user)
):
    """根据ID查询 {实体} 详情"""
    result = service.get_by_id(id)
    return BaseResponse(data=result)


@router.put(
    "/{id}",
    response_model=BaseResponse[{Entity}Response],
    summary="更新"
)
async def update_{entity}(
    id: int,
    data: {Entity}Update,
    service: {Entity}Service = Depends(get_service),
    current_user = Depends(get_current_user)
):
    """更新 {实体} 信息"""
    result = service.update(id, data)
    return BaseResponse(data=result)


@router.delete(
    "/{id}",
    response_model=BaseResponse,
    summary="删除"
)
async def delete_{entity}(
    id: int,
    service: {Entity}Service = Depends(get_service),
    current_user = Depends(get_current_user)
):
    """删除 {实体}"""
    service.delete(id)
    return BaseResponse(message="删除成功")
```

#### core/exceptions.py

```python
"""自定义异常"""


class AppException(Exception):
    """应用基础异常"""
    def __init__(self, message: str, code: int = 5000):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(AppException):
    """资源不存在"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code=4040)


class ConflictException(AppException):
    """资源冲突"""
    def __init__(self, message: str = "资源冲突"):
        super().__init__(message, code=4090)


class ValidationException(AppException):
    """参数校验失败"""
    def __init__(self, message: str = "参数校验失败"):
        super().__init__(message, code=4001)


class ForbiddenException(AppException):
    """权限不足"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, code=4030)
```

---

### Spring Boot (Java)

#### Entity.java

```java
package com.example.{feature}.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "{entity}s")
public class {Entity} {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String name;

    @Column(unique = true, length = 64)
    private String code;

    @Column(length = 32)
    private String status = "active";

    @Column(columnDefinition = "jsonb")
    private String metadata;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @Column
    private LocalDateTime deletedAt;

    // Getters and Setters
    // ...
}
```

#### {Entity}Service.java

```java
package com.example.{feature}.service;

import com.example.{feature}.dto.{Entity}CreateDTO;
import com.example.{feature}.dto.{Entity}UpdateDTO;
import com.example.{feature}.dto.{Entity}ResponseDTO;
import com.example.{feature}.entity.{Entity};
import com.example.{feature}.mapper.{Entity}Mapper;
import com.example.{feature}.repository.{Entity}Repository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class {Entity}Service {

    private final {Entity}Repository repository;
    private final {Entity}Mapper mapper;

    @Transactional
    public {Entity}ResponseDTO create({Entity}CreateDTO dto) {
        // 检查编码重复
        if (dto.getCode() != null && repository.existsByCode(dto.getCode())) {
            throw new ConflictException("编码已存在: " + dto.getCode());
        }

        {Entity} entity = mapper.toEntity(dto);
        entity = repository.save(entity);
        return mapper.toResponseDTO(entity);
    }

    @Transactional(readOnly = true)
    public {Entity}ResponseDTO getById(Long id) {
        {Entity} entity = repository.findByIdAndDeletedAtIsNull(id)
            .orElseThrow(() -> new NotFoundException("实体不存在: " + id));
        return mapper.toResponseDTO(entity);
    }

    @Transactional(readOnly = true)
    public Page<{Entity}ResponseDTO> getList(String status, String keyword, Pageable pageable) {
        // 查询逻辑
        return repository.findAll(pageable)
            .map(mapper::toResponseDTO);
    }

    @Transactional
    public {Entity}ResponseDTO update(Long id, {Entity}UpdateDTO dto) {
        {Entity} entity = repository.findByIdAndDeletedAtIsNull(id)
            .orElseThrow(() -> new NotFoundException("实体不存在: " + id));

        mapper.updateEntityFromDTO(dto, entity);
        entity = repository.save(entity);
        return mapper.toResponseDTO(entity);
    }

    @Transactional
    public void delete(Long id) {
        {Entity} entity = repository.findByIdAndDeletedAtIsNull(id)
            .orElseThrow(() -> new NotFoundException("实体不存在: " + id));
        entity.setDeletedAt(LocalDateTime.now());
    }
}
```

---

## 算法侧代码骨架

### C++17

#### 目录结构

```
algorithm/{feature}/
├── CMakeLists.txt               # 构建配置
├── include/
│   └── {feature}/
│       ├── {algorithm}.h        # 算法头文件
│       └── types.h              # 数据类型定义
├── src/
│   └── {algorithm}.cpp          # 算法实现
└── test/
    └── {algorithm}_test.cpp     # 单元测试
```

#### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)
project({feature}_algorithm VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 依赖库
find_package(OpenCV REQUIRED)
find_package(spdlog REQUIRED)

add_library({feature}_algorithm STATIC
    src/{algorithm}.cpp
)

target_include_directories({feature}_algorithm PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries({feature}_algorithm PUBLIC
    OpenCV::OpenCV
    spdlog::spdlog
)

# 测试
option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED)
    add_executable({algorithm}_test test/{algorithm}_test.cpp)
    target_link_libraries({algorithm}_test PRIVATE
        {feature}_algorithm
        GTest::GTest
    )
    add_test(NAME {algorithm}_test COMMAND {algorithm}_test)
endif()
```

#### include/{feature}/types.h

```cpp
#pragma once

#include <cstdint>
#include <chrono>
#include <optional>
#include <string>
#include <vector>

namespace {feature} {

// 状态枚举 — 对齐上游组件设计 [状态机: {Entity}StateMachine]
enum class {Entity}State : uint8_t {
    kInitialized = 0,   // 初始状态
    kProcessing  = 1,   // 处理中
    kCompleted   = 2,   // 已完成
    kFailed      = 3,   // 失败
};

// 输入数据结构 — 对齐上游接口设计 [接口: {Interface}.Input]
struct InputData {
    std::string source_id;      // 数据源标识
    std::vector<uint8_t> frame; // 帧数据
    std::chrono::milliseconds timestamp;
};

// 输出数据结构 — 对齐上游接口设计 [接口: {Interface}.Output]
struct OutputData {
    std::string target_id;      // 目标标识
    float confidence;           // 置信度 [0.0, 1.0]
    {Entity}State state;        // 当前状态
    std::string error_message;  // 错误信息（kFailed 时有效）
};

// 算法配置 — 对齐上游组件设计 [算法: {Algorithm}.Config]
struct AlgorithmConfig {
    float threshold = 0.75f;        // 判定阈值
    size_t max_retries = 3;         // 最大重试次数
    std::chrono::milliseconds timeout{5000}; // 超时时间
};

} // namespace {feature}
```

#### include/{feature}/{algorithm}.h

```cpp
#pragma once

#include "{feature}/types.h"
#include <optional>

namespace {feature} {

// {算法名称} — 对齐上游组件设计 [算法: {Algorithm}]
//
// 输入:  InputData  (帧数据 + 时间戳)
// 输出:  OutputData (识别结果 + 置信度 + 状态)
//
// 复杂度约束: O(n log n), n = 帧像素数
// 失败语义: 超时或置信度低于阈值时 state=kFailed
class {Algorithm} {
public:
    explicit {Algorithm}(AlgorithmConfig config = {});

    // 处理单帧数据
    auto Process(const InputData& input) -> OutputData;

    // 重置内部状态
    void Reset();

private:
    // 核心算法实现 — 上游算法锚点
    auto Compute(const std::vector<uint8_t>& frame) -> std::pair<float, std::string>;

    // 状态迁移 — 上游状态机锚点
    void Transition({Entity}State new_state);

    AlgorithmConfig config_;
    {Entity}State current_state_ = {Entity}State::kInitialized;
};

} // namespace {feature}
```

#### src/{algorithm}.cpp

```cpp
#include "{feature}/{algorithm}.h"
#include <spdlog/spdlog.h>

namespace {feature} {

{Algorithm}::{Algorithm}(AlgorithmConfig config)
    : config_(std::move(config)) {
    spdlog::info("{Algorithm} 初始化, threshold={}", config_.threshold);
}

auto {Algorithm}::Process(const InputData& input) -> OutputData {
    OutputData output{
        .target_id = input.source_id,
        .confidence = 0.0f,
        .state = {Entity}State::kProcessing,
    };

    // 异常处理锚点: 参考上游 [异常: InputData.Validation]
    if (input.frame.empty()) {
        spdlog::warn("空帧输入, source_id={}", input.source_id);
        output.state = {Entity}State::kFailed;
        output.error_message = "空帧输入";
        return output;
    }

    // 核心算法调用
    auto [confidence, error] = Compute(input.frame);

    if (!error.empty()) {
        spdlog::error("算法计算失败: {}", error);
        output.state = {Entity}State::kFailed;
        output.error_message = error;
        return output;
    }

    output.confidence = confidence;

    // 状态迁移: 参考上游 [状态机: {Entity}StateMachine.transition]
    if (confidence >= config_.threshold) {
        Transition({Entity}State::kCompleted);
    } else {
        Transition({Entity}State::kFailed);
        output.error_message = "置信度低于阈值";
    }

    output.state = current_state_;
    return output;
}

auto {Algorithm}::Compute(const std::vector<uint8_t>& frame)
    -> std::pair<float, std::string> {
    // 算法实现锚点: 上游组件设计 [算法: {Algorithm}.Compute]
    //
    // 输入: 帧像素数据
    // 输出: (置信度, 错误信息)
    // 复杂度: O(n log n)

    // TODO: 实现核心算法逻辑
    float confidence = 0.0f;
    // ... 算法处理逻辑 ...

    return {confidence, ""};
}

void {Algorithm}::Transition({Entity}State new_state) {
    // 状态机实现锚点: 上游组件设计 [状态机: {Entity}StateMachine]
    //
    // 合法迁移:
    //   kInitialized -> kProcessing -> kCompleted
    //                               -> kFailed
    //   kFailed -> kInitialized (Reset后)
    spdlog::debug("状态迁移: {} -> {}",
        static_cast<int>(current_state_),
        static_cast<int>(new_state));
    current_state_ = new_state;
}

void {Algorithm}::Reset() {
    current_state_ = {Entity}State::kInitialized;
    spdlog::debug("{Algorithm} 已重置");
}

} // namespace {feature}
```

#### test/{algorithm}_test.cpp

```cpp
#include <gtest/gtest.h>
#include "{feature}/{algorithm}.h"

namespace {feature} {
namespace {

TEST({Algorithm}Test, EmptyInputReturnsFailed) {
    {Algorithm} algo;
    InputData input{.source_id = "test", .frame = {}};
    auto output = algo.Process(input);
    EXPECT_EQ(output.state, {Entity}State::kFailed);
    EXPECT_FALSE(output.error_message.empty());
}

TEST({Algorithm}Test, ValidInputProducesConfidence) {
    {Algorithm} algo({Algorithm}Config{.threshold = 0.5f});
    InputData input{
        .source_id = "test",
        .frame = std::vector<uint8_t>(100, 0x80),
        .timestamp = std::chrono::milliseconds(1000)
    };
    auto output = algo.Process(input);
    // 正常输入应产生有效结果（具体断言依赖实际算法实现）
    EXPECT_GE(output.confidence, 0.0f);
    EXPECT_LE(output.confidence, 1.0f);
}

TEST({Algorithm}Test, ResetBringsBackToInitialized) {
    {Algorithm} algo;
    InputData input{.source_id = "test", .frame = {1, 2, 3}};
    algo.Process(input);
    algo.Reset();
    // 验证 Reset 后状态回归
    InputData input2{.source_id = "test2", .frame = {4, 5, 6}};
    auto output = algo.Process(input2);
    EXPECT_NE(output.state, {Entity}State::kInitialized); // 已重新处理
}

} // namespace
} // namespace {feature}
```

---

## 前端代码骨架

### Vue3 + TypeScript

#### 目录结构

```
src/
├── api/
│   └── {entity}.ts          # API 客户端
├── types/
│   └── {entity}.ts          # 类型定义
├── views/
│   └── {Feature}/
│       ├── index.vue        # 列表页面
│       ├── Detail.vue       # 详情页面
│       └── components/      # 子组件
│           ├── ListTable.vue
│           └── SearchForm.vue
└── composables/
    └── use{Entity}.ts       # 业务逻辑组合式函数
```

#### types/{entity}.ts

```typescript
"""{实体} 类型定义"""

export interface {Entity} {
  id: number
  name: string
  code?: string
  status: string
  metadata?: Record<string, any>
  createdAt: string
  updatedAt: string
}

export interface {Entity}CreateRequest {
  name: string
  code?: string
  status?: string
  metadata?: Record<string, any>
}

export interface {Entity}UpdateRequest {
  name?: string
  status?: string
  metadata?: Record<string, any>
}

export interface {Entity}ListResponse {
  items: {Entity}[]
  total: number
  page: number
  pageSize: number
}

export interface {Entity}ListParams {
  page?: number
  pageSize?: number
  status?: string
  keyword?: string
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}
```

#### api/{entity}.ts

```typescript
"""{实体} API 客户端"""
import request from '@/utils/request'
import type {
  {Entity},
  {Entity}CreateRequest,
  {Entity}UpdateRequest,
  {Entity}ListResponse,
  {Entity}ListParams
} from '@/types/{entity}'

const BASE_URL = '/api/v1/{features}'

export const {entity}Api = {
  /** 查询列表 */
  getList(params: {Entity}ListParams) {
    return request.get<{Entity}ListResponse>(BASE_URL, { params })
  },

  /** 查询详情 */
  getById(id: number) {
    return request.get<{Entity}>(`${BASE_URL}/${id}`)
  },

  /** 创建 */
  create(data: {Entity}CreateRequest) {
    return request.post<{Entity}>(BASE_URL, data)
  },

  /** 更新 */
  update(id: number, data: {Entity}UpdateRequest) {
    return request.put<{Entity}>(`${BASE_URL}/${id}`, data)
  },

  /** 删除 */
  delete(id: number) {
    return request.delete(`${BASE_URL}/${id}`)
  }
}
```

#### views/{Feature}/index.vue

```vue
<template>
  <div class="{feature}-page">
    <!-- 搜索表单 -->
    <SearchForm v-model="searchParams" @search="handleSearch" />

    <!-- 操作按钮 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建
      </el-button>
    </div>

    <!-- 数据表格 -->
    <ListTable
      :data="listData"
      :loading="loading"
      :pagination="pagination"
      @page-change="handlePageChange"
      @edit="handleEdit"
      @delete="handleDelete"
    />

    <!-- 编辑弹窗 -->
    <EditDialog
      v-model="dialogVisible"
      :data="currentRow"
      @success="handleSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import SearchForm from './components/SearchForm.vue'
import ListTable from './components/ListTable.vue'
import EditDialog from './components/EditDialog.vue'
import { {entity}Api } from '@/api/{entity}'
import type { {Entity}, {Entity}ListParams } from '@/types/{entity}'

// 搜索参数
const searchParams = reactive<{Entity}ListParams>({
  page: 1,
  pageSize: 20,
  status: undefined,
  keyword: ''
})

// 列表数据
const listData = ref<{Entity}[]>([])
const loading = ref(false)
const pagination = reactive({
  total: 0,
  page: 1,
  pageSize: 20
})

// 弹窗控制
const dialogVisible = ref(false)
const currentRow = ref<{Entity} | undefined>(undefined)

// 获取列表
const fetchList = async () => {
  loading.value = true
  try {
    const res = await {entity}Api.getList(searchParams)
    listData.value = res.items
    pagination.total = res.total
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.page = 1
  fetchList()
}

// 分页变化
const handlePageChange = (page: number, pageSize: number) => {
  searchParams.page = page
  searchParams.pageSize = pageSize
  fetchList()
}

// 新建
const handleCreate = () => {
  currentRow.value = undefined
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: {Entity}) => {
  currentRow.value = row
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row: {Entity}) => {
  try {
    await ElMessageBox.confirm('确定删除该记录吗？', '提示', {
      type: 'warning'
    })
    await {entity}Api.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch {
    // 取消删除
  }
}

// 操作成功
const handleSuccess = () => {
  dialogVisible.value = false
  fetchList()
}

// 初始化
onMounted(() => {
  fetchList()
})
</script>
```

---

## 代码规范说明

### 命名规范

| 类型 | 命名方式 | 示例 |
|------|----------|------|
| 类名 | PascalCase | `{Entity}Service` |
| 函数/方法 | snake_case / camelCase | `get_by_id`, `getById` |
| 变量 | snake_case / camelCase | `page_size`, `pageSize` |
| 常量 | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| 文件/目录 | snake_case / kebab-case | `{entity}_service.py`, `{feature}-list.vue` |

### 注释规范

```python
# 函数注释（Google风格）
def get_by_id(self, id: int) -> {Entity}:
    """根据ID查询实体

    Args:
        id: 实体ID

    Returns:
        实体对象

    Raises:
        NotFoundException: 实体不存在时抛出
    """
    pass
```

### 错误处理

```python
# 统一异常处理
from fastapi import HTTPException

@router.get("/{id}")
async def get_{entity}(id: int):
    try:
        return service.get_by_id(id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"查询失败: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误")
```
