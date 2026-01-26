# Skill: Form Handling (React Hook Form)

## Purpose
To manage form state, validation, and submission efficiently without causing excessive re-renders, unlike controlled components.

## When to Use
- Complex forms with many fields.
- Forms requiring validation rules (required, pattern, minLength).
- When performance is a concern (typing lag).

## Procedure
1.  **Initialize Hook**: `const { register, handleSubmit, formState: { errors } } = useForm();`.
2.  **Register Inputs**: Spread the register function onto inputs: `<input {...register("firstName", { required: true })} />`.
3.  **Handle Submit**: Pass your submit function to `handleSubmit`: `<form onSubmit={handleSubmit(onSubmit)}>`.
4.  **Display Errors**: Check the `errors` object: `{errors.firstName && <span>Required</span>}`.
5.  **Integrate UI Libraries**: Use `Controller` component for third-party inputs (Select, DatePicker) that don't expose a simple `ref`.

## Constraints
- Avoid mixing "controlled" and "uncontrolled" inputs manually; let the library handle it.
- Use a schema validator like `zod` via `@hookform/resolvers` for complex validation logic.

## Expected Output
A performant form component with built-in validation, error handling, and easy data submission.
