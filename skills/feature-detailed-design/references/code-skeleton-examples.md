# Feature 详细设计 - 代码骨架模板

## 目录

1. [后端代码骨架](#后端代码骨架)
   - [FastAPI (Python)](#fastapi-python)
   - [Spring Boot (Java)](#spring-boot-java)
2. [前端代码骨架](#前端代码骨架)
   - [Vue3 + TypeScript](#vue3--typescript)
3. [代码规范说明](#代码规范说明)

---

## 后端代码骨架

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
