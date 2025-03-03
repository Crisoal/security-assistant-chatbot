import React from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

// Define TypeScript types
interface SignUpFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

// Validation schema using Yup
const signupSchema = yup.object().shape({
  username: yup.string().required("Username is required"),
  email: yup
    .string()
    .email("Invalid email format")
    .required("Email is required"),
  password: yup
    .string()
    .min(6, "Password must be at least 6 characters")
    .required(),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref("password")], "Passwords do not match")
    .required("Confirm password is required"),
});

const SignUp: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpFormData>({
    resolver: yupResolver(signupSchema),
  });

  const onSubmit = (data: SignUpFormData) => {
    console.log("Signup Data:", data);
    alert("Signup successful! 🎉");
  };

  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input type="text" placeholder="Username" {...register("username")} />
        <p className="error">{errors.username?.message}</p>

        <input type="email" placeholder="Email" {...register("email")} />
        <p className="error">{errors.email?.message}</p>

        <input
          type="password"
          placeholder="Password"
          {...register("password")}
        />
        <p className="error">{errors.password?.message}</p>

        <input
          type="password"
          placeholder="Confirm Password"
          {...register("confirmPassword")}
        />
        <p className="error">{errors.confirmPassword?.message}</p>

        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
};

export default SignUp;
